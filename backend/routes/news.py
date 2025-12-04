from fastapi import APIRouter, HTTPException
from services.news_service import fetch_news
from services.yfinance_service import get_company_name

router = APIRouter()


@router.get("/news/{symbol}")
def news(symbol: str):
    try:
        # Get company name from yfinance for better news results
        company_name = get_company_name(symbol)
        articles = fetch_news(symbol, company_name)
        return {"symbol": symbol, "company_name": company_name, "articles": articles, "error": None}
    except Exception as e:
        return {"symbol": symbol, "company_name": None, "articles": [], "error": str(e)}


