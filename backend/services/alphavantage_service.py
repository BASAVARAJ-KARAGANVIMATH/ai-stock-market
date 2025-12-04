import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from backend directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def fetch_daily_adjusted(symbol: str):
    if not ALPHA_VANTAGE_KEY:
        return []  # Silent failure - no API key
    
    # Try common Indian suffix variants
    for candidate in _symbol_candidates(symbol):
        try:
            out = _fetch_daily(candidate)
            if out and len(out) > 0:
                return out
        except Exception:
            # Silent failure - try next candidate
            continue
    
    # All candidates failed - return empty, let route try next source
    return []


def fetch_overview(symbol: str):
    if not ALPHA_VANTAGE_KEY:
        return {} # No key, return empty gracefully
    last_error = None
    for candidate in _symbol_candidates(symbol):
        try:
            params = {
                "function": "OVERVIEW",
                "symbol": candidate,
                "apikey": ALPHA_VANTAGE_KEY,
            }
            r = requests.get(BASE_URL, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            
            # Check for rate limit
            if data.get("Note"):
                note = data["Note"]
                if "Thank you for using Alpha Vantage" in note or "rate limit" in note.lower():
                    raise ValueError("Alpha Vantage API rate limit reached. Please wait 1 minute and try again.")
                last_error = note
                continue
            
            # Check for error message
            if data.get("Error Message"):
                last_error = data["Error Message"]
                continue
            
            # Valid data must have Symbol field
            if data and data.get("Symbol"):
                return data
        except ValueError:
            # Re-raise rate limit errors
            raise
        except Exception as e:
            last_error = str(e)
            continue
    
    # Return empty dict but log the error if we have one
    if last_error:
        # Don't raise here - let the route handle it gracefully
        pass
    return {}


def _fetch_daily(symbol: str):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_KEY,
    }
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    response_keys = list(data.keys()) if isinstance(data, dict) else []
    
    # Check for Information key (can be rate limit or premium endpoint)
    if data.get("Information"):
        info = data["Information"]
        if "rate limit" in info.lower() or "25 requests per day" in info.lower():
            raise ValueError("Alpha Vantage daily rate limit reached (25 requests/day). The limit resets at midnight UTC or you can upgrade to premium.")
        if "premium" in info.lower() and "endpoint" in info.lower():
            raise ValueError(f"Premium endpoint required: {info}")
        # Other information messages
        raise ValueError(f"Alpha Vantage: {info}")
    
    # Check for rate limit or error messages FIRST
    if data.get("Note"):
        note = data["Note"]
        if "Thank you for using Alpha Vantage" in note or "rate limit" in note.lower():
            raise ValueError("Alpha Vantage API rate limit reached. Please wait 1 minute and try again.")
        raise ValueError(note)
    
    if data.get("Error Message"):
        raise ValueError(data["Error Message"])
    
    # Try to find the time series key - check all possible variations
    possible_keys = [
        "Time Series (Daily)",
        "Time Series Daily",
        "Daily Time Series"
    ]
    
    key = None
    for possible_key in possible_keys:
        # Check exact match first
        if possible_key in data:
            key = possible_key
            break
        # Check case-insensitive
        for actual_key in data.keys():
            if possible_key.lower() in actual_key.lower() or actual_key.lower() in possible_key.lower():
                key = actual_key
                break
        if key:
            break
    
    # If still not found, try to find any key containing "Time Series"
    if not key:
        for k in data.keys():
            if "time series" in k.lower() and "daily" in k.lower():
                key = k
                break
    
    if not key:
        # No valid time series data - return empty
        raise ValueError("No time series data")
    
    series = data[key]
    if not series or (isinstance(series, dict) and len(series) == 0):
        raise ValueError("Empty time series data from Alpha Vantage")
    
    if not isinstance(series, dict):
        raise ValueError(f"Time series data is not a dictionary. Got: {type(series)}")
    
    return _series_to_list(series, prefer_adjusted=False)


def _series_to_list(series: dict, prefer_adjusted: bool) -> list:
    out = []
    for date, row in series.items():
        close_key = "5. adjusted close" if prefer_adjusted else "4. close"
        out.append({
            "date": date,
            "open": safe_float(row.get("1. open", 0)),
            "high": safe_float(row.get("2. high", 0)),
            "low": safe_float(row.get("3. low", 0)),
            "close": safe_float(row.get(close_key, row.get("4. close", 0))),
            "volume": int(float(row.get("6. volume", 0) or 0))
        })
    out.sort(key=lambda x: x["date"], reverse=True)
    return out


def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None


def _symbol_candidates(symbol: str):
    sym = (symbol or "").strip().upper()
    sym = sym.replace(".NS", ".NSE").replace(".BO", ".BSE")
    has_suffix = sym.endswith(".NSE") or sym.endswith(".BSE")
    candidates = []
    if has_suffix:
        candidates.append(sym)
    else:
        # Try BSE then NSE by default
        candidates.extend([f"{sym}.BSE", f"{sym}.NSE"]) 
    # Also add swapped suffix order if provided
    if sym.endswith(".NSE"):
        candidates.append(sym.replace(".NSE", ".BSE"))
    if sym.endswith(".BSE"):
        candidates.append(sym.replace(".BSE", ".NSE"))
    # Ensure uniqueness
    seen = set()
    uniq = []
    for c in candidates:
        if c and c not in seen:
            uniq.append(c)
            seen.add(c)
    return uniq


def search_symbols(keywords: str):
    if not ALPHA_VANTAGE_KEY:
        return []
    
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords,
        "apikey": ALPHA_VANTAGE_KEY,
    }
    
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if "bestMatches" in data:
            # Filter for prefix matching (starts with)
            filtered = []
            kw = keywords.strip().lower()
            for m in data["bestMatches"]:
                sym = m.get("1. symbol", "").lower()
                name = m.get("2. name", "").lower()
                if sym.startswith(kw) or name.startswith(kw):
                    filtered.append(m)
            return filtered
        return []
    except Exception:
        # Silent failure
        return []



