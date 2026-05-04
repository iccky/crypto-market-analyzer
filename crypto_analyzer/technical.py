"""
Technical Indicators
RSI, EMA, SMA, MACD, Bollinger Bands, Fibonacci Retracement
"""

import numpy as np
from typing import List, Tuple


def safe_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """Calculate RSI (Relative Strength Index)."""
    if len(prices) < period + 1:
        return 50.0

    closes = np.array(prices[-period-1:])
    deltas = np.diff(closes)

    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)


def calculate_ema(prices: List[float], period: int) -> float:
    """Calculate EMA (Exponential Moving Average)."""
    if len(prices) < period:
        return prices[-1] if prices else 0.0

    arr = np.array(prices[-period:])
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    return float(np.convolve(arr, weights, mode='valid')[-1])


def calculate_sma(prices: List[float], period: int) -> float:
    """Calculate SMA (Simple Moving Average)."""
    if len(prices) < period:
        return prices[-1] if prices else 0.0
    return float(np.mean(prices[-period:]))


def calculate_macd(prices: List[float]) -> Tuple[float, float, float]:
    """Calculate MACD line, signal line, and histogram."""
    if len(prices) < 35:
        return 0.0, 0.0, 0.0

    def ema_series(data, period):
        k = 2 / (period + 1)
        ema = [data[0]]
        for price in data[1:]:
            ema.append(price * k + ema[-1] * (1 - k))
        return ema

    ema12 = ema_series(prices, 12)[-1]
    ema26 = ema_series(prices, 26)[-1]
    macd_line = ema12 - ema26

    macd_hist = [ema_series(prices, 12)[i] - ema_series(prices, 26)[i] for i in range(len(prices))]
    signal = ema_series(macd_hist, 9)[-1]
    histogram = macd_line - signal

    return float(macd_line), float(signal), float(histogram)


def calculate_bollinger_bands(prices: List[float], period: int = 20) -> Tuple[float, float, float]:
    """Returns (upper_band, middle_band, lower_band)."""
    if len(prices) < period:
        p = prices[-1] if prices else 0
        return p * 1.02, p, p * 0.98

    recent = np.array(prices[-period:])
    middle = np.mean(recent)
    std = np.std(recent)

    upper = middle + (2 * std)
    lower = middle - (2 * std)

    return float(upper), float(middle), float(lower)


def calculate_fibonacci_retracement(high: float, low: float) -> dict:
    """Calculate Fibonacci retracement levels."""
    diff = high - low
    levels = {
        '0.0': high,
        '0.236': high - (diff * 0.236),
        '0.382': high - (diff * 0.382),
        '0.5': high - (diff * 0.5),
        '0.618': high - (diff * 0.618),
        '0.786': high - (diff * 0.786),
        '1.0': low,
    }
    return {k: round(v, 4) for k, v in levels.items()}


def find_support_resistance(prices: List[float], window: int = 10) -> Tuple[float, float]:
    """Find nearest support and resistance levels using local min/max."""
    if len(prices) < window * 2:
        p = prices[-1] if prices else 0
        return p * 0.95, p * 1.05

    recent = prices[-window*3:]
    supports = []
    resistances = []

    for i in range(window, len(recent) - window):
        # Local minimum = support
        if all(recent[i] <= recent[i-j] for j in range(1, window+1)) and all(recent[i] <= recent[i+j] for j in range(1, window+1)):
            supports.append(recent[i])

        # Local maximum = resistance
        if all(recent[i] >= recent[i-j] for j in range(1, window+1)) and all(recent[i] >= recent[i+j] for j in range(1, window+1)):
            resistances.append(recent[i])

    current = prices[-1]
    support = max([s for s in supports if s < current], default=current * 0.95)
    resistance = min([r for r in resistances if r > current], default=current * 1.05)

    return float(support), float(resistance)


def calculate_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
    """Calculate Average True Range for volatility-based SL."""
    if len(closes) < period + 1:
        return closes[-1] * 0.03 if closes else 1.0

    tr_values = []
    for i in range(1, len(closes)):
        tr1 = highs[i] - lows[i]
        tr2 = abs(highs[i] - closes[i-1])
        tr3 = abs(lows[i] - closes[i-1])
        tr_values.append(max(tr1, tr2, tr3))

    return float(np.mean(tr_values[-period:]))


def get_trend_analysis(prices: List[float]) -> dict:
    """Comprehensive trend analysis."""
    if len(prices) < 30:
        return {'trend': 'NEUTRAL', 'strength': 0, 'description': 'Data insufficient'}

    ema9 = calculate_ema(prices, 9)
    ema21 = calculate_ema(prices, 21)
    ema50 = calculate_ema(prices, min(50, len(prices)))
    current = prices[-1]

    # Trend determination
    if ema9 > ema21 > ema50:
        trend = 'BULLISH'
        strength = min(abs(current - ema50) / ema50 * 100 * 5, 100)
    elif ema9 < ema21 < ema50:
        trend = 'BEARISH'
        strength = min(abs(current - ema50) / ema50 * 100 * 5, 100)
    else:
        trend = 'NEUTRAL'
        strength = 30

    # Price vs EMA position
    if current > ema9 > ema21:
        description = 'Strong uptrend, price above all EMAs'
    elif current < ema9 < ema21:
        description = 'Strong downtrend, price below all EMAs'
    elif ema9 > ema21 and current < ema9:
        description = 'Potential pullback in uptrend'
    elif ema9 < ema21 and current > ema9:
        description = 'Potential bounce in downtrend'
    else:
        description = 'Sideways consolidation'

    return {
        'trend': trend,
        'strength': round(strength, 1),
        'description': description,
        'ema9': round(ema9, 4),
        'ema21': round(ema21, 4),
        'ema50': round(ema50, 4),
    }
