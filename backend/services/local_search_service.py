import json
import os
from pathlib import Path

# Load data once at module level
DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'indian_stocks.json'

_STOCKS = []

def _load_stocks():
    global _STOCKS
    if not _STOCKS and DATA_PATH.exists():
        try:
            with open(DATA_PATH, 'r') as f:
                _STOCKS = json.load(f)
        except Exception as e:
            print(f"Error loading local stock data: {e}")

_load_stocks()

def search_local_symbols(query: str):
    """
    Search for stocks in the local list that match the query (prefix match).
    Returns a list of dicts formatted like Alpha Vantage results.
    """
    if not query:
        return []
    
    q = query.strip().lower()
    matches = []
    
    for stock in _STOCKS:
        symbol = stock.get("symbol", "")
        name = stock.get("name", "")
        
        # Check if symbol or name starts with query
        # Also check symbol without suffix (e.g. "TCS" matches "TCS.BSE")
        clean_symbol = symbol.split('.')[0]
        
        if (symbol.lower().startswith(q) or 
            name.lower().startswith(q) or 
            clean_symbol.lower().startswith(q)):
            
            matches.append({
                "1. symbol": symbol,
                "2. name": name,
                "3. type": "Equity",
                "4. region": "India",
                "8. currency": "INR"
            })
            
    return matches
