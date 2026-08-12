"""
Fetch stock ticker data using yfinance (Yahoo Finance).
"""

import logging
from typing import Dict, Any
import yfinance as yf


logger = logging.getLogger(__name__)


class TickerFetcher:
    """Fetch ticker data using yfinance."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
    
    def fetch(self) -> Dict[str, Any]:
        """
        Fetch current ticker data using yfinance.
        
        Returns:
            Dictionary with ticker data including current price, closing price, etc.
        """
        try:
            # Fetch ticker data using yfinance
            ticker_obj = yf.Ticker(self.ticker)
            
            # Get latest data
            info = ticker_obj.info
            history = ticker_obj.history(period='1d')
            
            if history.empty:
                raise ValueError(f"No data available for ticker {self.ticker}")
            
            latest_price = history['Close'].iloc[-1]
            
            return {
                'ticker': self.ticker,
                'current_price': float(info.get('currentPrice', latest_price)),
                'closing_price': float(latest_price),
                'previous_close': float(info.get('previousClose', 0)),
                'fifty_two_week_high': float(info.get('fiftyTwoWeekHigh', 0)),
                'fifty_two_week_low': float(info.get('fiftyTwoWeekLow', 0)),
                'market_cap': float(info.get('marketCap', 0)),
                'pe_ratio': float(info.get('trailingPE', 0)) if info.get('trailingPE') else None,
            }
            
        except Exception as e:
            logger.error(f"Error fetching ticker data for {self.ticker}: {str(e)}")
            raise


if __name__ == '__main__':
    # Test
    fetcher = TickerFetcher('AAPL')
    data = fetcher.fetch()
    print(data)
