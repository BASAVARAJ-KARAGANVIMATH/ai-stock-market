import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from services.yfinance_service import get_company_name
from services.news_service import fetch_news

def test_news_fetching(symbol):
    print(f"Testing for symbol: {symbol}")
    
    try:
        company_name = get_company_name(symbol)
        print(f"Company Name: {company_name}")
    except Exception as e:
        print(f"Error fetching company name: {e}")
        company_name = None

    try:
        articles = fetch_news(symbol, company_name)
        print(f"Found {len(articles)} articles.")
        for i, article in enumerate(articles[:3]):
            print(f"Article {i+1}: {article['title']}")
    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    test_news_fetching("WIPRO.NS")
    test_news_fetching("INFY.NS")
