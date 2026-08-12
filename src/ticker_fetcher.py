"""
Fetch stock ticker data from Yahoo Finance API.
"""

import os
import logging
import requests
from typing import Dict, Any


logger = logging.getLogger(__name__)


class TickerFetcher:
    """Fetch ticker data from Yahoo Finance."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.api_key = os.getenv('YAHOO_FINANCE_API_KEY')
        if not self.api_key:
            logger.warning("YAHOO_FINANCE_API_KEY not set, using free endpoint")
        self.base_url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary"
    
    def fetch(self) -> Dict[str, Any]:
        """
        Fetch current ticker data.
        
        Returns:
            Dictionary with ticker data including current price, closing price, etc.
        """
        try:
            # Using free Yahoo Finance endpoint (no API key required)
            url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}"
            
            params = {
                'modules': 'price,summaryDetail,financialData'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'quoteSummary' not in data or 'result' not in data['quoteSummary']:
                raise ValueError(f"Invalid response for ticker {self.ticker}")
            
            quote_data = data['quoteSummary']['result'][0]
            price_data = quote_data.get('price', {})
            
            return {
                'ticker': self.ticker,
                'current_price': price_data.get('currentPrice', {}).get('raw', 0),
                'closing_price': price_data.get('regularMarketPrice', {}).get('raw', 0),
                'previous_close': price_data.get('previousClose', {}).get('raw', 0),
                'fifty_two_week_high': price_data.get('fiftyTwoWeekHigh', {}).get('raw', 0),
                'fifty_two_week_low': price_data.get('fiftyTwoWeekLow', {}).get('raw', 0),
                'market_cap': price_data.get('marketCap', {}).get('raw', 0),
                'pe_ratio': price_data.get('trailingPE', {}).get('raw', None),
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching ticker data for {self.ticker}: {str(e)}")
            raise
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing ticker data: {str(e)}")
            raise


if __name__ == '__main__':
    # Test
    fetcher = TickerFetcher('AAPL')
    data = fetcher.fetch()
    print(data)
