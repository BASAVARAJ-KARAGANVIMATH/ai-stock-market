from fastapi import APIRouter, HTTPException
from services.alphavantage_service import fetch_daily_adjusted
from services.recommendation_service import generate_recommendation
from services.yfinance_service import fetch_yf_fundamentals, fetch_yf_daily
from services.nse_service import fetch_nse_daily
from ai_service import getAIRecommendation
from services.news_service import fetch_news

router = APIRouter()


@router.get("/predict/{symbol}")
async def predict(symbol: str):
    try:
        # 1. Fetch technical data (prices)
        # 1. Fetch technical data (prices) with fallback (YF -> AV -> NSE)
        prices = []
        try:
            prices = fetch_yf_daily(symbol)
        except Exception:
            pass
        
        if not prices:
            try:
                prices = fetch_daily_adjusted(symbol)
            except Exception:
                pass
        
        if not prices:
            try:
                prices = fetch_nse_daily(symbol)
            except Exception:
                pass
                
        if not prices:
            raise ValueError(f"Could not fetch price data for {symbol} from any source.")
        basic_result = generate_recommendation(prices)
        basic_result["symbol"] = symbol
        basic_result["error"] = None

        # 2. Fetch data needed for AI analysis
        raw_fundamentals = {}
        company_name = None
        try:
            raw_fundamentals = fetch_yf_fundamentals(symbol)
            # Extract company name from fundamentals for better news search
            company_name = raw_fundamentals.get("ShortName")
        except Exception:
            pass
        news = []
        try:
            news = fetch_news(symbol, company_name)
        except Exception:
            pass  # News is optional

        # 3. Get AI-driven recommendation
        ai_rec = await getAIRecommendation(prices, raw_fundamentals, news)

        return {
            "symbol": symbol,
            "basic_recommendation": basic_result,
            "ai_recommendation": ai_rec
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred for symbol {symbol}: {str(e)}")


