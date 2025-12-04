import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from services.yfinance_service import get_company_name

def test_name_fetching(symbol):
    print(f"Testing for symbol: {symbol}")
    try:
        company_name = get_company_name(symbol)
        print(f"Company Name: {company_name}")
    except Exception as e:
        print(f"Error fetching company name: {e}")

if __name__ == "__main__":
    test_name_fetching("WIPRO.NS")
    test_name_fetching("INFY.NS")
    test_name_fetching("TCS.NS")
