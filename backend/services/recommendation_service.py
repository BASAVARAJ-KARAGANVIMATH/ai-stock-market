from typing import Dict, List
from utils.indicators import rsi, simple_moving_average


def generate_recommendation(prices: List[Dict]):
    rsi_val = rsi(prices, period=14)
    sma_short = simple_moving_average(prices, window=20)
    sma_long = simple_moving_average(prices, window=50)

    # Placeholder rules
    if rsi_val is not None:
        if rsi_val < 30:
            rec = "Buy"
        elif rsi_val > 70:
            rec = "Sell"
        else:
            rec = "Hold"
    else:
        rec = "Hold"

    return {
        "recommendation": rec,
        "rsi": rsi_val,
        "sma_short": sma_short,
        "sma_long": sma_long,
    }


