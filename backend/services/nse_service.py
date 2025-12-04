from nsetools import Nse
from nsepython import nse_quote_ltp, equity_history
import datetime

nse = Nse()

# Basic price and fundamentals from nsetools (real-time)
def fetch_nse_fundamentals(symbol: str):
    symbol = symbol.replace('.NSE', '').replace('.BSE','')
    try:
        quote = nse.get_quote(symbol)
    except Exception as e:
        return {}
    out = {
        'pe_ratio': quote.get('pChange'), # Not exact, nsetools lacks P/E directly
        'eps': None,
        'market_cap': quote.get('marketCapitalization'),
        'price_to_book': None,
        'return_on_equity': None,
        'debt_to_equity': None,
        'dividend_yield': quote.get('dividendYield'),
        'high_52w': quote.get('high52'),
        'low_52w': quote.get('low52'),
        'name': quote.get('companyName'),
    }
    return out

def fetch_nse_daily(symbol: str, days: int = 365):
    nse = Nse()
    symbol_upper = symbol.split('.')[0].upper()
    # Fetch the daily chart data
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days)
    try:
        # equity_history returns a DataFrame
        df = equity_history(symbol_upper, "EQ", start.strftime("%d-%m-%Y"), today.strftime("%d-%m-%Y"))
        out = []
        for index, entry in df.iterrows():
            # Parse date from DD-Mon-YYYY to YYYY-MM-DD
            try:
                dt = datetime.datetime.strptime(entry["mTIMESTAMP"], "%d-%b-%Y").strftime("%Y-%m-%d")
            except:
                dt = str(entry["mTIMESTAMP"])
                
            out.append({
                "date": dt,
                "open": float(entry.get("CH_OPENING_PRICE", 0)),
                "high": float(entry.get("CH_TRADE_HIGH_PRICE", 0)),
                "low": float(entry.get("CH_TRADE_LOW_PRICE", 0)),
                "close": float(entry.get("CH_CLOSING_PRICE", 0)),
                "volume": int(entry.get("CH_TOT_TRADED_QTY", 0))
            })
        # equity_history might be sorted differently, ensure reverse chronological
        out.sort(key=lambda x: x["date"], reverse=True)
        return out
    except Exception as e:
        print(f"NSE Error: {e}")
        # As a last resort, return just empty list
        return []
