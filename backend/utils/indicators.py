from typing import List, Dict
import numpy as np
import pandas as pd


def to_series(prices: List[Dict]):
    # Expect prices sorted latest-first; convert to oldest-first for indicators
    df = pd.DataFrame(prices)
    df = df.sort_values("date")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"])  # keep only valid closes
    df = df.reset_index(drop=True)
    return df


def simple_moving_average(prices: List[Dict], window: int) -> float | None:
    df = to_series(prices)
    if len(df) < window:
        return None
    return float(df["close"].rolling(window=window).mean().iloc[-1])


def rsi(prices: List[Dict], period: int = 14) -> float | None:
    df = to_series(prices)
    if len(df) <= period:
        return None
    delta = df["close"].diff()
    gain = (delta.clip(lower=0)).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    out = 100 - (100 / (1 + rs))
    val = out.iloc[-1]
    return float(val) if pd.notna(val) else None


def moving_average_crossover(prices: List[Dict], short_window: int = 20, long_window: int = 50) -> str:
    short = simple_moving_average(prices, short_window)
    long = simple_moving_average(prices, long_window)
    if short is None or long is None:
        return "neutral"
    if short > long:
        return "bullish"
    if short < long:
        return "bearish"
    return "neutral"


def macd(prices: List[Dict], fast=12, slow=26, signal=9):
    df = to_series(prices)
    if len(df) < slow:
        return None
    exp1 = df["close"].ewm(span=fast, adjust=False).mean()
    exp2 = df["close"].ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return {
        "line": float(macd_line.iloc[-1]),
        "signal": float(signal_line.iloc[-1]),
        "hist": float(hist.iloc[-1])
    }

def bollinger_bands(prices: List[Dict], window=20, num_std=2):
    df = to_series(prices)
    if len(df) < window:
        return None
    sma = df["close"].rolling(window=window).mean()
    std = df["close"].rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return {
        "upper": float(upper.iloc[-1]),
        "middle": float(sma.iloc[-1]),
        "lower": float(lower.iloc[-1])
    }

def adx(prices: List[Dict], period=14):
    # Simplified ADX calculation
    df = to_series(prices)
    if len(df) < period + 1:
        return None
    
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    
    df['tr0'] = abs(df['high'] - df['low'])
    df['tr1'] = abs(df['high'] - df['close'].shift())
    df['tr2'] = abs(df['low'] - df['close'].shift())
    df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
    
    df['dm_plus'] = np.where((df['high'] - df['high'].shift()) > (df['low'].shift() - df['low']), 
                             np.maximum(df['high'] - df['high'].shift(), 0), 0)
    df['dm_minus'] = np.where((df['low'].shift() - df['low']) > (df['high'] - df['high'].shift()), 
                              np.maximum(df['low'].shift() - df['low'], 0), 0)
    
    atr = df['tr'].rolling(window=period).mean()
    plus_di = 100 * (df['dm_plus'].rolling(window=period).mean() / atr)
    minus_di = 100 * (df['dm_minus'].rolling(window=period).mean() / atr)
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx_val = dx.rolling(window=period).mean().iloc[-1]
    
    return float(adx_val) if pd.notna(adx_val) else None
