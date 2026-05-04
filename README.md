# Crypto Market Analyzer

**Analisis Teknikal Altcoin Otomatis dengan Rekomendasi Entry, Stop Loss, dan Take Profit.**

Dibangun dengan Python, menggunakan data real-time dari CoinGecko API.

---

## Fitur

- 🔍 **Pencarian Altcoin** — Cari coin berdasarkan nama atau symbol (BTC, ETH, SOL, dll)
- 📊 **Analisis Teknikal** — RSI, SMA/EMA, MACD, Bollinger Bands, Fibonacci Retracement
- 🎯 **Signal Generator** — Rekomendasi BUY/SELL/NEUTRAL dengan confidence score
- 💰 **Entry Calculator** — Harga entry optimal berdasarkan support/resistance
- 🛑 **Stop Loss & Take Profit** — Level SL/TP otomatis dengan risk-reward ratio
- 📈 **Trend Analysis** — Identifikasi trend (bullish/bearish/sideways)
- 🌐 **Data Real-time** — Harga live dari CoinGecko (gratis, no API key required)
- ⚡ **CLI Cepat** — Jalankan dari terminal, output rapi siap Telegram/Discord

---

## Instalasi

```bash
git clone https://github.com/iccky/crypto-market-analyzer.git
cd crypto-market-analyzer
pip install -r requirements.txt
```

---

## Penggunaan

### Analisis Single Coin

```bash
python -m crypto_analyzer.main solana
# atau
python -m crypto_analyzer.main bitcoin
```

### Output

```
═══════════════════════════════════════
🔍 ANALISIS TEKNIKAL: SOLANA (SOL)
═══════════════════════════════════════
💰 Harga Sekarang: $142.35
📊 Perubahan 24h: +3.45% 🟢
📈 Volume 24h: $2.8B

📐 TREND ANALYSIS
───────────────────────────────────────
🐂 Trend: BULLISH (EMA9 > EMA21)
📊 RSI(14): 62.3 — NORMAL
📈 MACD: BULLISH crossover

🎯 TRADE SETUP
───────────────────────────────────────
✅ SIGNAL: STRONG BUY (78% confidence)
💰 Entry: $138.50 — $140.20 (order limit)
🛑 Stop Loss: $131.50 (-5.0%)
🎯 Take Profit 1: $149.80 (+7.5%) | 1:1.5 RR
🎯 Take Profit 2: $156.40 (+12.0%) | 1:2.4 RR
🎯 Take Profit 3: $163.10 (+17.0%) | 1:3.4 RR

📊 RISK REWARD: 1:2.4 (TP2)
💡 Catatan: Entry di dekat support daily. Volume meningkat.
```

---

## Dependensi

| Package | Versi | Fungsi |
|---------|-------|--------|
| requests | >=2.28 | HTTP API calls |
| numpy | >=1.24 | Numerical computation |
| click | >=8.1 | CLI framework |
| colorama | >=0.4 | Terminal colors |

---

## Struktur Project

```
crypto-market-analyzer/
├── crypto_analyzer/
│   ├── __init__.py
│   ├── api.py          # CoinGecko API wrapper
│   ├── technical.py    # Indicators (RSI, MACD, Fibonacci, etc)
│   ├── signals.py      # Signal generator + entry/SL/TP calculator
│   ├── formatter.py    # Output formatting (Telegram-ready)
│   └── main.py         # CLI entry point
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore
```

---

## API Sumber Data

**CoinGecko Public API** (gratis, rate limit: 10-30 calls/min)
- `/coins/markets` — Harga & market data
- `/coins/{id}/market_chart` — Historical OHLCV
- `/search` — Pencarian coin

---

## Disclaimer

⚠️ **NOT FINANCIAL ADVICE.** Tool ini untuk edukasi dan riset saja. Selalu lakukan due diligence sebelum trading. Cryptocurrency sangat volatile. Past performance tidak menjamin hasil masa depan.

---

## Lisensi

MIT License — bebas digunakan, dimodifikasi, dan didistribusikan.

---

🚀 **Built with Python + CoinGecko API**

---

## 🚀 Deploy ke Vercel (Serverless)

### Langkah 1: Install Vercel CLI
```bash
npm i -g vercel
```

### Langkah 2: Login ke Vercel
```bash
vercel login
```

### Langkah 3: Deploy
```bash
cd crypto-market-analyzer
vercel --prod
```

### Struktur Vercel
```
crypto-market-analyzer/
├── api/
│   └── index.py          # Flask app untuk Vercel Serverless
├── crypto_analyzer/      # Core modules
│   ├── api.py
│   ├── technical.py
│   ├── signals.py
│   └── formatter.py
├── vercel.json           # Vercel config
├── requirements.txt      # Dependencies (include Flask)
└── README.md
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface (HTML) |
| `/api/analyze/{coin}` | GET | Analisis teknikal coin |
| `/api/top/{limit}` | GET | Top coins by market cap |
| `/api/trending` | GET | Trending coins |

### Contoh API Call
```bash
curl https://your-project.vercel.app/api/analyze/solana
```

Response:
```json
{
  "coin_id": "solana",
  "name": "Solana",
  "symbol": "SOL",
  "current_price": 142.35,
  "signal": {
    "signal": "STRONG_BUY",
    "confidence": 78,
    "rsi": 62.3,
    "trend": { "trend": "BULLISH", "strength": 85 }
  },
  "setup": {
    "side": "LONG",
    "entry_zone_low": 138.50,
    "entry_zone_high": 140.20,
    "stop_loss": 131.50,
    "take_profit_1": 149.80,
    "take_profit_2": 156.40,
    "take_profit_3": 163.10
  }
}
```
