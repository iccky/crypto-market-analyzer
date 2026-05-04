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
