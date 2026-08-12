"""
Log market analysis results to CSV file.
"""

import os
import logging
import csv
from datetime import datetime
from typing import Dict, Any
from pathlib import Path


logger = logging.getLogger(__name__)


class CSVLogger:
    """Log market analysis results to CSV."""
    
    def __init__(self, csv_path: str = 'data/market_analysis.csv'):
        self.csv_path = csv_path
        self.ensure_directory()
        self.ensure_headers()
    
    def ensure_directory(self):
        """Ensure the data directory exists."""
        directory = os.path.dirname(self.csv_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def ensure_headers(self):
        """Ensure CSV file has headers."""
        if not os.path.exists(self.csv_path):
            headers = [
                'Timestamp',
                'Ticker',
                'Current_Price',
                'Closing_Price',
                'SMA_Weekly',
                'SMA_Monthly',
                'SMA_Quarterly',
                'vs_Weekly_Percent',
                'vs_Monthly_Percent',
                'vs_Quarterly_Percent',
                'News_Count',
                'AI_Commentary',
                'Analysis_Status'
            ]
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
            logger.info(f"Created CSV file: {self.csv_path}")
    
    def log_analysis(self, report_data: Dict[str, Any]):
        """
        Log analysis results to CSV.
        
        Args:
            report_data: Dictionary containing analysis results
        """
        try:
            row = {
                'Timestamp': report_data.get('timestamp', datetime.now().isoformat()),
                'Ticker': report_data.get('ticker', ''),
                'Current_Price': report_data.get('current_price', ''),
                'Closing_Price': report_data.get('closing_price', ''),
                'SMA_Weekly': report_data.get('sma_weekly', ''),
                'SMA_Monthly': report_data.get('sma_monthly', ''),
                'SMA_Quarterly': report_data.get('sma_quarterly', ''),
                'vs_Weekly_Percent': report_data.get('vs_weekly_percent', ''),
                'vs_Monthly_Percent': report_data.get('vs_monthly_percent', ''),
                'vs_Quarterly_Percent': report_data.get('vs_quarterly_percent', ''),
                'News_Count': report_data.get('news_count', 0),
                'AI_Commentary': report_data.get('ai_commentary', '')[:200],  # Truncate for CSV
                'Analysis_Status': 'Success'
            }
            
            # Get headers from existing file
            headers = self._get_headers()
            
            # Append row to CSV
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerow(row)
            
            logger.info(f"Logged analysis for {report_data.get('ticker')} to {self.csv_path}")
            
        except Exception as e:
            logger.error(f"Error logging to CSV: {str(e)}")
            raise
    
    def _get_headers(self):
        """Get headers from existing CSV file."""
        try:
            with open(self.csv_path, 'r') as f:
                reader = csv.reader(f)
                return next(reader)
        except Exception:
            return [
                'Timestamp', 'Ticker', 'Current_Price', 'Closing_Price',
                'SMA_Weekly', 'SMA_Monthly', 'SMA_Quarterly',
                'vs_Weekly_Percent', 'vs_Monthly_Percent', 'vs_Quarterly_Percent',
                'News_Count', 'AI_Commentary', 'Analysis_Status'
            ]
    
    def log_error(self, ticker: str, error_message: str):
        """Log an error to CSV."""
        try:
            row = {
                'Timestamp': datetime.now().isoformat(),
                'Ticker': ticker,
                'Current_Price': '',
                'Closing_Price': '',
                'SMA_Weekly': '',
                'SMA_Monthly': '',
                'SMA_Quarterly': '',
                'vs_Weekly_Percent': '',
                'vs_Monthly_Percent': '',
                'vs_Quarterly_Percent': '',
                'News_Count': 0,
                'AI_Commentary': error_message[:200],
                'Analysis_Status': 'Error'
            }
            
            headers = self._get_headers()
            
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerow(row)
            
            logger.info(f"Logged error for {ticker}")
            
        except Exception as e:
            logger.error(f"Error logging to CSV: {str(e)}")


if __name__ == '__main__':
    # Test
    logger_obj = CSVLogger()
    test_data = {
        'timestamp': datetime.now().isoformat(),
        'ticker': 'AAPL',
        'current_price': 153.50,
        'closing_price': 152.80,
        'sma_weekly': 151.20,
        'sma_monthly': 150.50,
        'sma_quarterly': 148.00,
        'vs_weekly_percent': 1.52,
        'vs_monthly_percent': 1.99,
        'vs_quarterly_percent': 3.65,
        'news_count': 3,
        'ai_commentary': 'Stock is in an uptrend with positive momentum.'
    }
    logger_obj.log_analysis(test_data)
