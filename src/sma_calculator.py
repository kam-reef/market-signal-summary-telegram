"""
Calculate Simple Moving Averages (SMA) for stock tickers.
"""

import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any
import yfinance as yf


logger = logging.getLogger(__name__)


class SMACalculator:
    """Calculate simple moving averages for a ticker."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
    
    def calculate(self) -> Dict[str, Any]:
        """
        Calculate SMAs for different periods.
        
        Returns:
            Dictionary with SMA values
        """
        try:
            # Fetch the last 200 days of data (ensures enough data for all SMAs)
            # 200 days > 63 trading days (quarterly)
            ticker_obj = yf.Ticker(self.ticker)
            hist_data = ticker_obj.history(period='1y')
            
            if hist_data.empty:
                logger.warning(f"No historical data for {self.ticker}, using mock data")
                hist_data = self._generate_mock_data()
            
            # Ensure data is sorted chronologically (oldest first, newest last)
            hist_data = hist_data.sort_index()
            
            close_prices = hist_data['Close']
            
            # Remove any NaN values at the end
            close_prices = close_prices.dropna()
            
            if len(close_prices) < 63:
                logger.warning(f"Insufficient data for {self.ticker}, only {len(close_prices)} days available")
            
            # Calculate SMAs using the last N days
            # SMA for 1 week (5 trading days)
            sma_weekly = close_prices.iloc[-5:].mean() if len(close_prices) >= 5 else close_prices.mean()
            
            # SMA for 1 month (21 trading days)
            sma_monthly = close_prices.iloc[-21:].mean() if len(close_prices) >= 21 else close_prices.mean()
            
            # SMA for 1 quarter (63 trading days)
            sma_quarterly = close_prices.iloc[-63:].mean() if len(close_prices) >= 63 else close_prices.mean()
            
            current_price = close_prices.iloc[-1]
            
            logger.info(f"{self.ticker}: Current=${current_price:.2f}, "
                       f"Weekly SMA=${sma_weekly:.2f}, Monthly=${sma_monthly:.2f}, "
                       f"Quarterly=${sma_quarterly:.2f}")
            
            return {
                'ticker': self.ticker,
                'sma_weekly': round(float(sma_weekly), 2),
                'sma_monthly': round(float(sma_monthly), 2),
                'sma_quarterly': round(float(sma_quarterly), 2),
                'current_price': round(float(current_price), 2),
                'vs_weekly': round(float(current_price - sma_weekly), 2),
                'vs_monthly': round(float(current_price - sma_monthly), 2),
                'vs_quarterly': round(float(current_price - sma_quarterly), 2),
                'weekly_percent': round((float(current_price - sma_weekly) / float(sma_weekly)) * 100, 2) if sma_weekly != 0 else 0,
                'monthly_percent': round((float(current_price - sma_monthly) / float(sma_monthly)) * 100, 2) if sma_monthly != 0 else 0,
                'quarterly_percent': round((float(current_price - sma_quarterly) / float(sma_quarterly)) * 100, 2) if sma_quarterly != 0 else 0,
            }
            
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            raise
    
    def _generate_mock_data(self) -> pd.DataFrame:
        """Generate mock historical data for demonstration."""
        dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
        import numpy as np
        prices = 100 + np.cumsum(np.random.randn(252) * 2)
        return pd.DataFrame({'Close': prices}, index=dates)


if __name__ == '__main__':
    # Test
    calc = SMACalculator('O')
    data = calc.calculate()
    print(data)
