from fastapi import APIRouter, HTTPException
from services.alphavantage_service import fetch_daily_adjusted, fetch_overview, search_symbols
from services.yfinance_service import fetch_yf_daily, fetch_yf_fundamentals
from services.nse_service import fetch_nse_daily, fetch_nse_fundamentals
from utils.fundamentals import analyze_fundamentals

router = APIRouter()

from services.local_search_service import search_local_symbols

@router.get("/stock/search")
def search_stock(query: str):
    if not query:
        return []
    
    # 1. Try local search first (fast, reliable for Indian stocks)
    local_matches = search_local_symbols(query)
    
    # 2. If we have enough local matches, return them to save API calls
    # You can adjust this threshold. If user types specific symbol not in local, 
    # we might still want to hit API. But for single letters like "T", local is best.
    if len(local_matches) >= 5:
        return format_results(local_matches)

    # 3. If not enough local matches, try Alpha Vantage
    try:
        api_matches = search_symbols(query)
    except Exception as e:
        print(f"Alpha Vantage search error: {e}")
        api_matches = []

    # Combine results, prioritizing local
    # Use a dict to deduplicate by symbol
    combined = {}
    for m in local_matches:
        combined[m["1. symbol"]] = m
    
    for m in api_matches:
        if m["1. symbol"] not in combined:
            combined[m["1. symbol"]] = m
            
    return format_results(list(combined.values()))

def format_results(matches):
    results = []
    for m in matches:
        results.append({
            "symbol": m.get("1. symbol"),
            "name": m.get("2. name"),
            "type": m.get("3. type"),
            "region": m.get("4. region"),
            "currency": m.get("8. currency"),
        })
    return results


@router.get("/stock/{symbol}")
def get_stock(symbol: str):
    prices = []
    overview = {}
    company_name = None
    fundamentals = {
        "pe_ratio": None,
        "eps": None,
        "market_cap": None,
        "price_to_book": None,
        "return_on_equity": None,
        "debt_to_equity": None,
        "dividend_yield": None,
        "high_52w": None,
        "low_52w": None,
        "name": None,
    }

    # 1. Try Alpha Vantage (silently)
    try:
        prices = fetch_daily_adjusted(symbol)
    except Exception:
        pass  # Silent - will try next source
    
    try:
        overview = fetch_overview(symbol)
    except Exception:
        overview = {}
    
    if overview:
        company_name = overview.get("Name")
        fundamentals.update({
            "pe_ratio": safe_float(overview.get("PERatio")),
            "eps": safe_float(overview.get("EPS")),
            "market_cap": safe_float(overview.get("MarketCapitalization")),
            "high_52w": safe_float(overview.get("52WeekHigh")),
            "low_52w": safe_float(overview.get("52WeekLow")),
            "price_to_book": safe_float(overview.get("PriceToBookRatio")),
            "return_on_equity": safe_float(overview.get("ReturnOnEquityTTM")),
            "return_on_assets": safe_float(overview.get("ReturnOnAssetsTTM")),
            "profit_margin": safe_float(overview.get("ProfitMargin")),
            "operating_margin": safe_float(overview.get("OperatingMarginTTM")),
            "debt_to_equity": safe_float(overview.get("DebtToEquityRatio")) or safe_float(overview.get("DebtToEquity")),
            "dividend_yield": safe_float(overview.get("DividendYield")),
            "ev_to_ebitda": safe_float(overview.get("EVToEBITDA")),
            "quarterly_earnings_growth_yoy": safe_float(overview.get("QuarterlyEarningsGrowthYOY")),
            "quarterly_revenue_growth_yoy": safe_float(overview.get("QuarterlyRevenueGrowthYOY")),
            "beta": safe_float(overview.get("Beta")),
            "industry_pe": safe_float(overview.get("IndustryPE")),
            "book_value": safe_float(overview.get("BookValue")),
            "face_value": safe_float(overview.get("FaceValue")),
        })

    # 2. If AV fails, try yfinance (silently)
    if not prices:
        try:
            prices = fetch_yf_daily(symbol)
        except Exception:
            pass  # Silent - will try next source
    
    # Try yfinance fundamentals IF missing key metrics
    if all(fundamentals[k] is None for k in ("pe_ratio","eps","market_cap")):
        try:
            yf_fund = fetch_yf_fundamentals(symbol)
            if yf_fund:
                fundamentals.update({k: v for k, v in yf_fund.items() if v is not None})
                if yf_fund.get("name"):
                    company_name = yf_fund["name"]
        except Exception:
            pass  # Silent

    # 3. If both fail, try NSE (silently)
    if not prices:
        try:
            prices = fetch_nse_daily(symbol)
        except Exception:
            pass  # Silent
    
    # Try NSE fundamentals IF missing key metrics
    if all(fundamentals[k] is None for k in ("pe_ratio","eps","market_cap")):
        try:
            nse_fund = fetch_nse_fundamentals(symbol)
            if nse_fund:
                fundamentals.update({k: v for k, v in nse_fund.items() if v is not None})
                if nse_fund.get("name"):
                    company_name = nse_fund["name"]
        except Exception:
            pass  # Silent

    # Determine if we have ANY usable data
    has_price_data = len(prices) > 0
    has_fundamental_data = any(fundamentals[k] is not None for k in ("pe_ratio", "eps", "market_cap"))
    
    # Only show error if EVERYTHING failed
    error_message = None
    if not has_price_data and not has_fundamental_data:
        error_message = "Data is temporarily unavailable for this ticker. Try again later or use a different stock symbol."
    
    analysis = analyze_fundamentals(fundamentals)
    latest_price = prices[0]["close"] if prices else None
    
    return {
        "symbol": symbol,
        "company_name": company_name,
        "price": latest_price,
        "fundamentals": fundamentals,
        "fundamental_analysis": analysis,
        "prices": prices,
        "error": error_message,  # Single clean error message or None
    }

def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None


