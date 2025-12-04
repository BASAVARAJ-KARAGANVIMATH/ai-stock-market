import yfinance as yf
import requests_cache
import datetime

# Install a cache for yfinance requests
# This will create a 'yfinance.cache' 
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'


def fetch_yf_daily(symbol: str, days: int = 365):
    try:
        # yfinance symbols: 'RELIANCE.NS', 'TCS.NS', etc.
        yf_symbol = symbol
        if symbol.endswith('.BSE'):
            yf_symbol = symbol.replace('.BSE', '.BO')
        elif symbol.endswith('.NSE'):
            yf_symbol = symbol.replace('.NSE', '.NS')
        ticker = yf.Ticker(yf_symbol)
        hist = ticker.history(period=f'{days}d')
        if hist.empty:
            return []
        result = []
        for date, row in hist.iterrows():
            result.append({
                "date": str(date.date()),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume'])
            })
        result.reverse()  # most recent last
        return result
    except Exception:
        # Silent failure - return empty, let route try next source
        return []

def get_company_name(symbol: str):
    """Extract just the company name from yfinance for a given symbol."""
    try:
        yf_symbol = symbol
        if symbol.endswith('.BSE'):
            yf_symbol = symbol.replace('.BSE', '.BO')
        elif symbol.endswith('.NSE'):
            yf_symbol = symbol.replace('.NSE', '.NS')
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info
        # Try multiple name fields in order of preference
        return info.get("longName") or info.get("shortName") or None
    except Exception:
        return None

def fetch_yf_fundamentals(symbol: str):
    try:
        yf_symbol = symbol
        if symbol.endswith('.BSE'):
            yf_symbol = symbol.replace('.BSE', '.BO')
        elif symbol.endswith('.NSE'):
            yf_symbol = symbol.replace('.NSE', '.NS')
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info
        
        # Calculate dividend yield manually to avoid unit ambiguity
        div_yield = info.get("dividendYield")
        if info.get("dividendRate") and info.get("currentPrice"):
            div_yield = info.get("dividendRate") / info.get("currentPrice")
        elif info.get("dividendRate") and info.get("previousClose"):
            div_yield = info.get("dividendRate") / info.get("previousClose")

        return {
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "return_on_equity": info.get("returnOnEquity"),
            "return_on_assets": info.get("returnOnAssets"),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "dividend_yield": div_yield,
            "debt_to_equity": info.get("debtToEquity"),
            "price_to_book": info.get("priceToBook"),
            "ev_to_ebitda": info.get("enterpriseToEbitda"),
            "quarterly_earnings_growth_yoy": info.get("earningsQuarterlyGrowth"),
            "quarterly_revenue_growth_yoy": info.get("revenueQuarterlyGrowth"),
            "beta": info.get("beta"),
            "market_cap": info.get("marketCap"),
            "high_52w": info.get("fiftyTwoWeekHigh"),
            "low_52w": info.get("fiftyTwoWeekLow"),
            "name": info.get("shortName"),
            "industry_pe": info.get("industryPE"),
            "book_value": info.get("bookValue"),
            "face_value": info.get("faceValue"),
        }
    except Exception:
        # Silent failure - return empty dict
        return {}

