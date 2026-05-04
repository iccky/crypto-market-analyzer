"""
Output Formatter
Formats analysis results into beautiful Telegram/Discord-ready messages.
"""

from typing import Dict


def format_analysis(result: Dict) -> str:
    """Format full analysis as Telegram message."""
    if 'error' in result:
        return f"❌ *Error:* {result['error']}"

    name = result.get('name', 'Unknown')
    symbol = result.get('symbol', '')
    price = result.get('current_price', 0)
    signal = result.get('signal', {})
    setup = result.get('setup', {})
    fib = result.get('fibonacci', {})
    market = result.get('market_data', {})

    sig = signal.get('signal', 'NEUTRAL')
    conf = signal.get('confidence', 0)
    rsi = signal.get('rsi', 50)

    # Signal emoji
    sig_emoji = {
        'STRONG_BUY': '🟢🟢', 'BUY': '🟢',
        'STRONG_SELL': '🔴🔴', 'SELL': '🔴',
        'NEUTRAL': '⚪'
    }.get(sig, '⚪')

    # Price change
    chg_24h = market.get('price_change_24h', 0)
    chg_emoji = '🟢' if chg_24h >= 0 else '🔴'

    lines = [
        f"{sig_emoji} *ANALISIS TEKNIKAL: {name} ({symbol})* {sig_emoji}",
        '',
        '═' * 40,
        '📊 *DATA PASAR*',
        '═' * 40,
        f"💰 Harga Sekarang: ${price:,.4f}",
        f"{chg_emoji} Perubahan 24h: {chg_24h:+.2f}%",
        f"📈 Volume 24h: ${market.get('total_volume', 0)/1e6:.1f}M",
        f"🏦 Market Cap: ${market.get('market_cap', 0)/1e6:.1f}M",
        f"📊 ATH: ${market.get('ath', 0):,.4f} | ATL: ${market.get('atl', 0):,.6f}",
        '',
        '═' * 40,
        '📐 *INDIKATOR TEKNIKAL*',
        '═' * 40,
    ]

    # RSI
    rsi_status = 'OVERBOUGHT' if rsi > 70 else 'OVERSOLD' if rsi < 30 else 'NORMAL'
    rsi_emoji = '🔴' if rsi > 70 else '🟢' if rsi < 30 else '⚪'
    lines.append(f"{rsi_emoji} RSI(14): {rsi} — {rsi_status}")

    # MACD
    macd = signal.get('macd', {})
    macd_emoji = '🟢' if macd.get('hist', 0) > 0 else '🔴'
    lines.append(f"{macd_emoji} MACD: {macd.get('hist', 0):+.4f} ({'Bullish' if macd.get('hist', 0) > 0 else 'Bearish'})")

    # Trend
    trend = signal.get('trend', {})
    trend_emoji = {'BULLISH': '🐂', 'BEARISH': '🐻', 'NEUTRAL': '⚖️'}.get(trend.get('trend'), '⚖️')
    lines.append(f"{trend_emoji} Trend: {trend.get('trend', 'NEUTRAL')} ({trend.get('strength', 0)}% strength)")
    lines.append(f"📍 EMA9: ${trend.get('ema9', 0):,.4f} | EMA21: ${trend.get('ema21', 0):,.4f}")

    # Bollinger
    bb = signal.get('bollinger', {})
    lines.append(f"📊 Bollinger: ${bb.get('lower', 0):,.4f} — ${bb.get('upper', 0):,.4f}")

    lines.append('')
    lines.append('═' * 40)
    lines.append(f"🎯 *SIGNAL: {sig} ({conf}% confidence)*")
    lines.append('═' * 40)

    # Signal reasons
    for reason in signal.get('reasons', []):
        lines.append(f"  ✅ {reason}")

    lines.append('')
    lines.append('═' * 40)
    lines.append('💰 *TRADE SETUP*')
    lines.append('═' * 40)
    lines.append(f"📌 Side: {setup.get('side', '—')}")
    lines.append(f"💰 Entry Zone: ${setup.get('entry_zone_low', 0):,.4f} — ${setup.get('entry_zone_high', 0):,.4f}")
    lines.append(f"🛑 Stop Loss: ${setup.get('stop_loss', 0):,.4f} ({setup.get('risk_pct', 0):.1f}% risk)")
    lines.append(f"🎯 TP1: ${setup.get('take_profit_1', 0):,.4f} | RR: 1:{setup.get('rr_tp1', 0)}")
    lines.append(f"🎯 TP2: ${setup.get('take_profit_2', 0):,.4f} | RR: 1:{setup.get('rr_tp2', 0)}")
    lines.append(f"🎯 TP3: ${setup.get('take_profit_3', 0):,.4f} | RR: 1:{setup.get('rr_tp3', 0)}")

    # Key levels
    lines.append('')
    lines.append('═' * 40)
    lines.append('📍 *KEY LEVELS*')
    lines.append('═' * 40)
    lines.append(f"🟢 Support: ${signal.get('support', 0):,.4f}")
    lines.append(f"🔴 Resistance: ${signal.get('resistance', 0):,.4f}")
    lines.append(f"📊 ATR(14): ${result.get('atr', 0):,.4f}")

    # Fibonacci
    lines.append('')
    lines.append('═' * 40)
    lines.append('📐 *FIBONACCI RETRACEMENT*')
    lines.append('═' * 40)
    for level, value in fib.items():
        star = '⭐' if level in ['0.618', '0.5'] else '  '
        lines.append(f"{star} {level}: ${value:,.4f}")

    lines.append('')
    lines.append('─' * 40)
    lines.append('⚠️ *DISCLAIMER:* Ini bukan financial advice.')
    lines.append('Selalu lakukan riset sendiri sebelum trading.')
    lines.append('─' * 40)

    return '\n'.join(lines)


def format_compact(result: Dict) -> str:
    """Compact one-line format for quick overview."""
    if 'error' in result:
        return f"❌ {result['error']}"

    symbol = result.get('symbol', '')
    price = result.get('current_price', 0)
    sig = result.get('signal', {}).get('signal', 'NEUTRAL')
    conf = result.get('signal', {}).get('confidence', 0)
    setup = result.get('setup', {})

    emoji = {'STRONG_BUY': '🟢🟢', 'BUY': '🟢', 'SELL': '🔴', 'STRONG_SELL': '🔴🔴', 'NEUTRAL': '⚪'}.get(sig, '⚪')

    return (
        f"{emoji} *{symbol}* @ ${price:,.4f} | "
        f"{sig} ({conf}%) | "
        f"SL: ${setup.get('stop_loss', 0):,.4f} | "
        f"TP2: ${setup.get('take_profit_2', 0):,.4f}"
    )


def format_top_coins(coins: list, limit: int = 10) -> str:
    """Format top coins table."""
    lines = [
        f"📊 *TOP {limit} COINS BY MARKET CAP*",
        '═' * 45,
        "#  Symbol    Price        24h      Cap",
        '─' * 45,
    ]

    for i, coin in enumerate(coins[:limit], 1):
        symbol = coin.get('symbol', '').upper()[:6]
        price = coin.get('current_price', 0)
        chg = coin.get('price_change_percentage_24h', 0)
        mcap = coin.get('market_cap', 0) / 1e9
        emoji = '🟢' if chg >= 0 else '🔴'

        lines.append(
            f"{i:2d} {symbol:8s} ${price:10,.2f} {emoji} {chg:+6.2f}% ${mcap:8.1f}B"
        )

    return '\n'.join(lines)
