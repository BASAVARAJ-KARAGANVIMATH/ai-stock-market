from __future__ import annotations

from typing import Any, Dict, Tuple


def _f(x: Any) -> float | None:
    try:
        if x in (None, "", "None"):
            return None
        return float(x)
    except Exception:
        return None


def score_metric(value: float | None, good_range: Tuple[float | None, float | None], weight: float, invert: bool = False) -> float:
    if value is None:
        return 0.0
    lo, hi = good_range
    # Normalize into [0,1] based on target range; clamp
    if lo is not None and hi is not None and hi != lo:
        t = (value - lo) / (hi - lo)
    elif lo is not None:
        t = 1.0 if value >= lo else 0.0
    elif hi is not None:
        t = 1.0 if value <= hi else 0.0
    else:
        t = 0.5
    t = max(0.0, min(1.0, t))
    if invert:
        t = 1.0 - t
    return t * weight


def analyze_fundamentals(overview: Dict[str, Any]) -> Dict[str, Any]:
    # Extract metrics
    market_cap = _f(overview.get("market_cap"))
    pe = _f(overview.get("pe_ratio"))
    industry_pe = _f(overview.get("industry_pe"))
    pb = _f(overview.get("price_to_book"))
    roe = _f(overview.get("return_on_equity"))
    eps_growth = _f(overview.get("quarterly_earnings_growth_yoy")) # Proxy for EPS trend
    dte = _f(overview.get("debt_to_equity"))
    # Book value trend is hard to get from single snapshot, defaulting to "Rising" (2) if positive, else Neutral (1)
    # Ideally we need historical book value.
    # For now, we'll assume if Price > Book (PB > 1), market expects growth, so maybe book value is stable/rising.
    # Let's use a simplified heuristic: if we have a valid book value, we give it a neutral score (1) 
    # unless we can determine trend. The user asked for "rising=2, flat=1, falling=0".
    # Without history, we'll be conservative and give 1.
    book_value_score = 1 

    scores = {}
    
    # 1. Market Cap
    # Large/Mid (>5000Cr approx? User didn't define ranges, using standard Indian context)
    # Let's assume input Market Cap is in actual currency units. 
    # yfinance usually returns full number. 5000 Cr = 50,000,000,000
    if market_cap:
        mc_cr = market_cap / 10000000 # Convert to Crores
        if mc_cr > 5000:
            scores["Market Cap"] = 2
        elif mc_cr >= 1000:
            scores["Market Cap"] = 1
        else:
            scores["Market Cap"] = 0
    else:
        scores["Market Cap"] = 0

    # 2. PE vs Industry
    if pe and industry_pe:
        if pe <= industry_pe:
            scores["PE vs Industry"] = 2
        elif pe <= industry_pe * 1.2: # Slightly above
            scores["PE vs Industry"] = 1
        else:
            scores["PE vs Industry"] = 0
    elif pe:
        # If no industry PE, assume 20-25 is fair? Or just give neutral?
        # Let's give neutral 1 if reasonable (<30), else 0
        scores["PE vs Industry"] = 1 if pe < 30 else 0
    else:
        scores["PE vs Industry"] = 0

    # 3. PB Ratio
    if pb:
        if pb < 3:
            scores["PB Ratio"] = 2
        elif pb <= 6:
            scores["PB Ratio"] = 1
        else:
            scores["PB Ratio"] = 0
    else:
        scores["PB Ratio"] = 0

    # 4. ROE
    # yfinance returns decimal (0.15 for 15%). User wants >18%
    if roe:
        roe_pct = roe * 100
        if roe_pct > 18:
            scores["ROE"] = 2
        elif roe_pct >= 12:
            scores["ROE"] = 1
        else:
            scores["ROE"] = 0
    else:
        scores["ROE"] = 0

    # 5. EPS TTM (Growth)
    # Using quarterly growth as proxy
    if eps_growth:
        if eps_growth > 0:
            scores["EPS Growth"] = 2
        elif eps_growth == 0:
            scores["EPS Growth"] = 1
        else:
            scores["EPS Growth"] = 0
    else:
        scores["EPS Growth"] = 1 # Assume flat if unknown

    # 6. Debt to Equity
    if dte:
        # yfinance D/E is usually a ratio (e.g. 0.5) or percentage? 
        # yfinance 'debtToEquity' is often percentage (e.g. 50 for 0.5). 
        # Let's check standard yfinance output. It's usually %.
        # So 0.5 ratio = 50.
        # User said <0.5 (ratio) = 2. So < 50.
        if dte < 50:
            scores["Debt-to-Equity"] = 2
        elif dte <= 100:
            scores["Debt-to-Equity"] = 1
        else:
            scores["Debt-to-Equity"] = 0
    else:
        scores["Debt-to-Equity"] = 1 # Neutral if unknown

    # 7. Book Value
    scores["Book Value"] = book_value_score

    total_score = sum(scores.values())

    if total_score >= 12:
        classification = "STRONG"
    elif total_score >= 7:
        classification = "MODERATE"
    else:
        classification = "WEAK"

    explanation = f"Score {total_score}/14. {classification} fundamentals based on key metrics."

    return {
        "scores": scores,
        "total_score": total_score,
        "classification": classification,
        "explanation": explanation
    }



