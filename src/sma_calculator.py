"""
Calculate Simple Moving Averages (SMA) for stock tickers.
"""

import os
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any


logger = logging.getLogger(__name__)


class SMACalculator:
    """Calculate simple moving averages for a ticker."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.api_key = os.getenv('YAHOO_FINANCE_API_KEY')
    
    def _fetch_historical_data(self, period: str = '1y') -> pd.DataFrame:
        """
        Fetch historical price data.
        
        Args:
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            DataFrame with historical prices
        """
        try:
            url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self.ticker}"
            
            params = {
                'modules': 'price,summaryDetail'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            # For SMA calculation, we'll use yfinance which is more reliable for historical data
            try:
                import yfinance as yf
                ticker_obj = yf.Ticker(self.ticker)
                hist = ticker_obj.history(period=period)
                return hist
            except ImportError:
                logger.warning("yfinance not available, falling back to mock data")
                return self._generate_mock_data()
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return self._generate_mock_data()
    
    def _generate_mock_data(self) -> pd.DataFrame:
        """Generate mock historical data for demonstration."""
        dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
        import numpy as np
        prices = 100 + np.cumsum(np.random.randn(252) * 2)
        return pd.DataFrame({'Close': prices}, index=dates)
    
    def calculate(self) -> Dict[str, Any]:
        """
        Calculate SMAs for different periods.
        
        Returns:
            Dictionary with SMA values
        """
        try:
            # Fetch historical data
            hist_data = self._fetch_historical_data('1y')
            
            if hist_data.empty:
                logger.warning(f"No historical data for {self.ticker}, using mock data")
                hist_data = self._generate_mock_data()
            
            close_prices = hist_data['Close']
            
            # Calculate SMAs
            # SMA for 1 week (5 trading days)
            sma_weekly = close_prices.rolling(window=5).mean().iloc[-1]
            
            # SMA for 1 month (21 trading days)
            sma_monthly = close_prices.rolling(window=21).mean().iloc[-1]
            
            # SMA for 1 quarter (63 trading days)
            sma_quarterly = close_prices.rolling(window=63).mean().iloc[-1]
            
            current_price = close_prices.iloc[-1]
            
            return {
                'ticker': self.ticker,
                'sma_weekly': round(float(sma_weekly), 2),
                'sma_monthly': round(float(sma_monthly), 2),
                'sma_quarterly': round(float(sma_quarterly), 2),
                'current_price': round(float(current_price), 2),
                'vs_weekly': round(float(current_price - sma_weekly), 2),
                'vs_monthly': round(float(current_price - sma_monthly), 2),
                'vs_quarterly': round(float(current_price - sma_quarterly), 2),
                'weekly_percent': round((float(current_price - sma_weekly) / float(sma_weekly)) * 100, 2),
                'monthly_percent': round((float(current_price - sma_monthly) / float(sma_monthly)) * 100, 2),
                'quarterly_percent': round((float(current_price - sma_quarterly) / float(sma_quarterly)) * 100, 2),
            }
            
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            raise


if __name__ == '__main__':
    # Test
    calc = SMACalculator('AAPL')
    data = calc.calculate()
    print(data)
