"""
CoinGecko API Wrapper
Free public API, no key required (rate limit: 10-30 calls/min)
"""

import requests
import time
from typing import Optional, List, Dict

BASE_URL = 'https://api.coingecko.com/api/v3'


class CoinGeckoAPI:
    """Low-level CoinGecko API client with rate limiting."""

    def __init__(self):
        self.session = requests.Session()
        self.last_call = 0
        self.min_interval = 2.0  # seconds between calls (safe for free tier)

    def _rate_limit(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        self._rate_limit()
        url = f"{BASE_URL}{endpoint}"
        resp = self.session.get(url, params=params or {}, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # ─── Public Methods ──────────────────────────────────────────

    def search(self, query: str) -> List[Dict]:
        """Search coins by name or symbol."""
        data = self._get('/search', {'query': query})
        return data.get('coins', [])

    def get_coin_data(self, coin_id: str) -> Dict:
        """Get full coin data (price, market cap, volume, etc)."""
        return self._get(
            f'/coins/{coin_id}',
            {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false',
            }
        )

    def get_market_chart(self, coin_id: str, days: int = 30, vs_currency: str = 'usd') -> Dict:
        """Get OHLCV market chart data."""
        return self._get(
            f'/coins/{coin_id}/market_chart',
            {'vs_currency': vs_currency, 'days': days}
        )

    def get_ohlc(self, coin_id: str, days: int = 30, vs_currency: str = 'usd') -> List[List]:
        """Get OHLC candlestick data [[timestamp, open, high, low, close], ...]."""
        # CoinGecko OHLC endpoint
        data = self._get(
            f'/coins/{coin_id}/ohlc',
            {'vs_currency': vs_currency, 'days': days}
        )
        return data

    def get_trending(self) -> List[Dict]:
        """Get trending coins (top 7)."""
        data = self._get('/search/trending')
        return data.get('coins', [])

    def get_top_coins(self, limit: int = 50, vs_currency: str = 'usd') -> List[Dict]:
        """Get top coins by market cap."""
        return self._get(
            '/coins/markets',
            {
                'vs_currency': vs_currency,
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': 1,
                'sparkline': 'false',
                'price_change_percentage': '1h,24h,7d',
            }
        )
