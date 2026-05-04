"""
Signal Generator & Trade Setup Calculator
Generates BUY/SELL signals and calculates optimal Entry, SL, TP levels.
"""

from typing import Dict, List, Tuple
from .technical import (
    calculate_rsi, calculate_macd, calculate_bollinger_bands,
    calculate_fibonacci_retracement, find_support_resistance,
    get_trend_analysis, calculate_atr, calculate_ema
)


def generate_signal(prices: List[float], highs: List[float], lows: List[float],
                    coin_data: dict) -> dict:
    """Generate trading signal with confidence score."""
    if not prices or len(prices) < 30:
        return {'signal': 'NEUTRAL', 'confidence': 0, 'reason': 'Insufficient data'}

    current = prices[-1]

    # Technical indicators
    rsi = calculate_rsi(prices)
    macd_line, signal_line, hist = calculate_macd(prices)
    upper, middle, lower = calculate_bollinger_bands(prices)
    trend = get_trend_analysis(prices)
    support, resistance = find_support_resistance(prices)

    # Score components (0-100)
    score = 0
    reasons = []

    # RSI scoring
    if rsi < 30:
        score += 25
        reasons.append(f'RSI oversold ({rsi:.1f})')
    elif rsi < 40:
        score += 15
        reasons.append(f'RSI near oversold ({rsi:.1f})')
    elif rsi > 70:
        score -= 25
        reasons.append(f'RSI overbought ({rsi:.1f})')
    elif rsi > 60:
        score -= 10
        reasons.append(f'RSI elevated ({rsi:.1f})')
    else:
        score += 5
        reasons.append(f'RSI neutral ({rsi:.1f})')

    # MACD scoring
    if hist > 0 and macd_line > signal_line:
        score += 20
        reasons.append('MACD bullish crossover')
    elif hist < 0 and macd_line < signal_line:
        score -= 20
        reasons.append('MACD bearish crossover')
    elif hist > 0:
        score += 10
        reasons.append('MACD positive histogram')
    else:
        score -= 10
        reasons.append('MACD negative histogram')

    # Trend scoring
    if trend['trend'] == 'BULLISH':
        score += 20
        reasons.append(f"Trend bullish ({trend['strength']:.0f}% strength)")
    elif trend['trend'] == 'BEARISH':
        score -= 20
        reasons.append(f"Trend bearish ({trend['strength']:.0f}% strength)")
    else:
        reasons.append('Trend neutral')

    # Price vs Bollinger Bands
    if current <= lower:
        score += 15
        reasons.append('Price at lower Bollinger Band')
    elif current >= upper:
        score -= 15
        reasons.append('Price at upper Bollinger Band')

    # Volume check (if available)
    vol_24h = coin_data.get('total_volume', 0)
    mcap = coin_data.get('market_cap', 1)
    if vol_24h and mcap:
        vol_ratio = vol_24h / mcap
        if vol_ratio > 0.1:
            score += 5
            reasons.append('High volume activity')

    # Determine signal
    if score >= 50:
        signal = 'STRONG_BUY' if score >= 70 else 'BUY'
    elif score <= -50:
        signal = 'STRONG_SELL' if score <= -70 else 'SELL'
    else:
        signal = 'NEUTRAL'

    confidence = min(abs(score), 100)

    return {
        'signal': signal,
        'confidence': confidence,
        'score': score,
        'reasons': reasons,
        'rsi': round(rsi, 1),
        'macd': {'line': round(macd_line, 4), 'signal': round(signal_line, 4), 'hist': round(hist, 4)},
        'bollinger': {'upper': round(upper, 4), 'middle': round(middle, 4), 'lower': round(lower, 4)},
        'trend': trend,
        'support': round(support, 4),
        'resistance': round(resistance, 4),
    }


def calculate_trade_setup(current_price: float, support: float, resistance: float,
                         signal: str, atr: float = None) -> dict:
    """Calculate optimal entry, stop loss, and take profit levels."""

    is_long = signal in ['BUY', 'STRONG_BUY']

    if is_long:
        # Entry zone: between support and current price
        entry_zone_low = min(support * 1.01, current_price * 0.97)
        entry_zone_high = min(current_price * 1.005, resistance * 0.95)
        entry_zone_high = max(entry_zone_high, entry_zone_low * 1.01)

        # Stop Loss: below support or ATR-based
        if atr:
            sl = min(support * 0.98, current_price - (atr * 2))
        else:
            sl = support * 0.98

        # Take Profits based on risk-reward ratios
        risk = entry_zone_high - sl
        if risk <= 0:
            risk = current_price * 0.03

        tp1 = entry_zone_high + (risk * 1.5)
        tp2 = entry_zone_high + (risk * 2.5)
        tp3 = entry_zone_high + (risk * 4.0)

    else:  # SHORT
        entry_zone_low = max(resistance * 0.99, current_price * 0.995)
        entry_zone_high = max(current_price * 1.03, resistance * 1.01)

        if atr:
            sl = max(resistance * 1.02, current_price + (atr * 2))
        else:
            sl = resistance * 1.02

        risk = sl - entry_zone_low
        if risk <= 0:
            risk = current_price * 0.03

        tp1 = entry_zone_low - (risk * 1.5)
        tp2 = entry_zone_low - (risk * 2.5)
        tp3 = entry_zone_low - (risk * 4.0)

    # Calculate risk-reward for each TP
    def calc_rr(tp, entry, sl_price):
        risk = abs(entry - sl_price)
        reward = abs(tp - entry)
        return round(reward / risk, 2) if risk > 0 else 0

    entry_display = (entry_zone_low + entry_zone_high) / 2

    return {
        'entry_zone_low': round(entry_zone_low, 4),
        'entry_zone_high': round(entry_zone_high, 4),
        'entry': round(entry_display, 4),
        'stop_loss': round(sl, 4),
        'take_profit_1': round(tp1, 4),
        'take_profit_2': round(tp2, 4),
        'take_profit_3': round(tp3, 4),
        'rr_tp1': calc_rr(tp1, entry_display, sl),
        'rr_tp2': calc_rr(tp2, entry_display, sl),
        'rr_tp3': calc_rr(tp3, entry_display, sl),
        'risk_pct': round(abs(sl - entry_display) / entry_display * 100, 2),
        'side': 'LONG' if is_long else 'SHORT',
    }


def analyze_coin(coin_id: str, api_client) -> dict:
    """Full analysis pipeline for a coin."""

    # Get coin data
    coin_data = api_client.get_coin_data(coin_id)
    market = coin_data.get('market_data', {})

    current_price = safe_float(market.get('current_price', {}).get('usd'))
    if not current_price:
        return {'error': 'Could not fetch price data'}

    # Get historical data for indicators
    chart = api_client.get_market_chart(coin_id, days=60)
    prices = [p[1] for p in chart.get('prices', [])]
    market_caps = [m[1] for m in chart.get('market_caps', [])]
    volumes = [v[1] for v in chart.get('total_volumes', [])]

    if len(prices) < 30:
        return {'error': 'Insufficient historical data'}

    # Calculate highs and lows from price data (approximation)
    highs = [max(prices[max(0, i-3):i+1]) for i in range(len(prices))]
    lows = [min(prices[max(0, i-3):i+1]) for i in range(len(prices))]

    # Generate signal
    coin_summary = {
        'current_price': current_price,
        'total_volume': market.get('total_volume', {}).get('usd', 0),
        'market_cap': market.get('market_cap', {}).get('usd', 1),
        'price_change_24h': market.get('price_change_percentage_24h', 0),
        'price_change_7d': market.get('price_change_percentage_7d', 0),
        'ath': market.get('ath', {}).get('usd', 0),
        'atl': market.get('atl', {}).get('usd', 0),
    }

    signal_data = generate_signal(prices, highs, lows, coin_summary)

    # Calculate trade setup
    atr = calculate_atr(highs, lows, prices) if len(highs) > 14 else current_price * 0.03
    setup = calculate_trade_setup(
        current_price,
        signal_data['support'],
        signal_data['resistance'],
        signal_data['signal'],
        atr
    )

    # Fibonacci levels
    recent_high = max(prices[-30:])
    recent_low = min(prices[-30:])
    fib = calculate_fibonacci_retracement(recent_high, recent_low)

    return {
        'coin_id': coin_id,
        'name': coin_data.get('name', coin_id),
        'symbol': coin_data.get('symbol', '').upper(),
        'current_price': current_price,
        'market_data': coin_summary,
        'signal': signal_data,
        'setup': setup,
        'fibonacci': fib,
        'atr': round(atr, 4),
    }


def safe_float(val, default=0.0):
    try:
        return float(val)
    except (TypeError, ValueError):
        return default
