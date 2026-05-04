"""
Vercel Serverless API
Flask app untuk deployment di Vercel
"""

from flask import Flask, request, jsonify, render_template_string
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_analyzer.api import CoinGeckoAPI
from crypto_analyzer.signals import analyze_coin

app = Flask(__name__)


def create_html():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Market Analyzer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); min-height: 100vh; color: #fff; }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        h1 { text-align: center; font-size: 2.5rem; margin-bottom: 10px; background: linear-gradient(90deg, #00d4ff, #7b2cbf); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { text-align: center; color: #8892b0; margin-bottom: 40px; }
        .search-box { display: flex; gap: 10px; margin-bottom: 30px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); }
        input { flex: 1; padding: 14px 20px; border: none; border-radius: 12px; background: rgba(255,255,255,0.1); color: #fff; font-size: 16px; outline: none; }
        input::placeholder { color: #8892b0; }
        button { padding: 14px 30px; border: none; border-radius: 12px; background: linear-gradient(135deg, #00d4ff, #7b2cbf); color: #fff; font-size: 16px; font-weight: 600; cursor: pointer; transition: transform 0.2s; }
        button:hover { transform: translateY(-2px); }
        .loading { text-align: center; padding: 40px; display: none; }
        .loading.active { display: block; }
        .spinner { width: 50px; height: 50px; border: 3px solid rgba(255,255,255,0.1); border-top-color: #00d4ff; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .result { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); display: none; }
        .result.active { display: block; }
        .signal-badge { display: inline-block; padding: 8px 20px; border-radius: 20px; font-weight: 700; font-size: 14px; margin-bottom: 20px; }
        .signal-STRONG_BUY { background: rgba(0, 255, 0, 0.2); color: #00ff88; }
        .signal-BUY { background: rgba(0, 255, 0, 0.15); color: #00ff88; }
        .signal-SELL { background: rgba(255, 0, 0, 0.15); color: #ff4757; }
        .signal-STRONG_SELL { background: rgba(255, 0, 0, 0.2); color: #ff4757; }
        .signal-NEUTRAL { background: rgba(255, 255, 255, 0.1); color: #8892b0; }
        .price-display { font-size: 3rem; font-weight: 700; margin-bottom: 5px; }
        .price-change { font-size: 1.2rem; margin-bottom: 20px; }
        .positive { color: #00ff88; } .negative { color: #ff4757; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .card { background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; }
        .card-label { color: #8892b0; font-size: 12px; text-transform: uppercase; margin-bottom: 5px; }
        .card-value { font-size: 1.3rem; font-weight: 600; }
        .trade-setup { background: rgba(0, 212, 255, 0.05); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 12px; padding: 20px; margin-top: 20px; }
        .trade-setup h3 { color: #00d4ff; margin-bottom: 15px; font-size: 1.2rem; }
        .level-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .level-label { color: #8892b0; } .level-value { font-weight: 600; font-family: monospace; }
        .level-value.entry { color: #00d4ff; } .level-value.sl { color: #ff4757; } .level-value.tp { color: #00ff88; }
        .confidence-bar { height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin: 10px 0 20px; }
        .confidence-fill { height: 100%; background: linear-gradient(90deg, #00d4ff, #7b2cbf); border-radius: 4px; transition: width 0.5s; }
        .error { background: rgba(255, 0, 0, 0.1); border: 1px solid rgba(255, 0, 0, 0.3); color: #ff4757; padding: 20px; border-radius: 12px; text-align: center; display: none; }
        .error.active { display: block; }
        .indicators { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 20px 0; }
        .indicator { background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; text-align: center; }
        .indicator-name { font-size: 11px; color: #8892b0; text-transform: uppercase; }
        .indicator-value { font-size: 1.1rem; font-weight: 600; margin-top: 5px; }
        .footer { text-align: center; margin-top: 40px; color: #8892b0; font-size: 12px; }
        .api-link { color: #00d4ff; text-decoration: none; } .api-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Crypto Market Analyzer</h1>
        <p class="subtitle">Technical Analysis & Trade Setup for Altcoins</p>
        <div class="search-box">
            <input type="text" id="coinInput" placeholder="Enter coin name (bitcoin, solana, eth...)" onkeypress="if(event.key==='Enter')analyze()">
            <button onclick="analyze()">Analyze</button>
        </div>
        <div class="loading" id="loading"><div class="spinner"></div><p>Analyzing...</p></div>
        <div class="error" id="error"></div>
        <div class="result" id="result"></div>
        <div class="footer">
            <p>Powered by CoinGecko | <a href="/api/analyze/bitcoin" class="api-link">API</a> | <a href="https://github.com/iccky/crypto-market-analyzer" class="api-link">GitHub</a></p>
        </div>
    </div>
    <script>
        async function analyze() {
            const coin = document.getElementById('coinInput').value.trim();
            if (!coin) return;
            document.getElementById('loading').classList.add('active');
            document.getElementById('result').classList.remove('active');
            document.getElementById('error').classList.remove('active');
            try {
                const res = await fetch('/api/analyze/' + coin);
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                render(data);
            } catch (e) {
                document.getElementById('error').textContent = e.message;
                document.getElementById('error').classList.add('active');
            } finally {
                document.getElementById('loading').classList.remove('active');
            }
        }
        function render(d) {
            const s = d.signal || {}, st = d.setup || {}, m = d.market_data || {};
            const chg = (m.price_change_24h || 0) >= 0 ? 'positive' : 'negative';
            document.getElementById('result').innerHTML = `
                <div style="text-align:center;margin-bottom:20px;">
                    <span class="signal-badge signal-${s.signal || 'NEUTRAL'}">${s.signal || 'NEUTRAL'}</span>
                    <div class="confidence-bar"><div class="confidence-fill" style="width:${s.confidence || 0}%"></div></div>
                    <p style="color:#8892b0;font-size:14px;">Confidence: ${s.confidence || 0}%</p>
                </div>
                <div style="text-align:center;">
                    <div class="price-display">$${d.current_price.toLocaleString('en-US',{minimumFractionDigits:4,maximumFractionDigits:4})}</div>
                    <div class="price-change ${chg}">${(m.price_change_24h || 0).toFixed(2)}% (24h)</div>
                </div>
                <div class="grid">
                    <div class="card"><div class="card-label">Volume 24h</div><div class="card-value">$${((m.total_volume || 0)/1e6).toFixed(1)}M</div></div>
                    <div class="card"><div class="card-label">Market Cap</div><div class="card-value">$${((m.market_cap || 0)/1e6).toFixed(1)}M</div></div>
                    <div class="card"><div class="card-label">ATH</div><div class="card-value">$${(m.ath || 0).toLocaleString()}</div></div>
                </div>
                <div class="indicators">
                    <div class="indicator"><div class="indicator-name">RSI(14)</div><div class="indicator-value">${s.rsi || '-'}</div></div>
                    <div class="indicator"><div class="indicator-name">Trend</div><div class="indicator-value">${(s.trend || {}).trend || '-'}</div></div>
                    <div class="indicator"><div class="indicator-name">MACD</div><div class="indicator-value">${(s.macd || {}).hist > 0 ? 'Bullish' : 'Bearish'}</div></div>
                    <div class="indicator"><div class="indicator-name">ATR(14)</div><div class="indicator-value">$${(d.atr || 0).toFixed(4)}</div></div>
                </div>
                <div class="trade-setup">
                    <h3>Trade Setup (${st.side || '-'})</h3>
                    <div class="level-row"><span class="level-label">Entry Zone</span><span class="level-value entry">$${(st.entry_zone_low || 0).toFixed(4)} - $${(st.entry_zone_high || 0).toFixed(4)}</span></div>
                    <div class="level-row"><span class="level-label">Stop Loss</span><span class="level-value sl">$${(st.stop_loss || 0).toFixed(4)} (${(st.risk_pct || 0).toFixed(1)}% risk)</span></div>
                    <div class="level-row"><span class="level-label">TP1</span><span class="level-value tp">$${(st.take_profit_1 || 0).toFixed(4)} (1:${st.rr_tp1 || 0})</span></div>
                    <div class="level-row"><span class="level-label">TP2</span><span class="level-value tp">$${(st.take_profit_2 || 0).toFixed(4)} (1:${st.rr_tp2 || 0})</span></div>
                    <div class="level-row"><span class="level-label">TP3</span><span class="level-value tp">$${(st.take_profit_3 || 0).toFixed(4)} (1:${st.rr_tp3 || 0})</span></div>
                </div>
                <div style="margin-top:20px;padding:15px;background:rgba(255,255,255,0.03);border-radius:12px;">
                    <h4 style="color:#8892b0;margin-bottom:10px;">Signal Reasons</h4>
                    ${(s.reasons || []).map(r => `<p style="margin:5px 0;font-size:14px;">✅ ${r}</p>`).join('')}
                </div>`;
            document.getElementById('result').classList.add('active');
        }
    </script>
</body>
</html>'''


@app.route('/')
def index():
    return render_template_string(create_html())


@app.route('/api/analyze/<coin>')
def api_analyze(coin):
    try:
        api = CoinGeckoAPI()
        results = api.search(coin)
        if not results:
            return jsonify({'error': f"Coin '{coin}' not found"}), 404
        result = analyze_coin(results[0]['id'], api)
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/top/<int:limit>')
def api_top(limit):
    try:
        api = CoinGeckoAPI()
        return jsonify(api.get_top_coins(limit=min(limit, 100)))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trending')
def api_trending():
    try:
        api = CoinGeckoAPI()
        return jsonify(api.get_trending())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Vercel entry point
app = app
