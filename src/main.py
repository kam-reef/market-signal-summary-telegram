#!/usr/bin/env python3
"""
Main orchestrator for market analysis workflow.
Coordinates data fetching, analysis, and reporting.
"""

import argparse
import logging
import sys
import os
from datetime import datetime

from ticker_fetcher import TickerFetcher
from sma_calculator import SMACalculator
from news_fetcher import NewsFetcher
from ai_commentary import AICommentary
from csv_logger import CSVLogger
from telegram_reporter import TelegramReporter


def setup_logging():
    """Set up logging configuration."""
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/market_analysis.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Market Analysis Workflow')
    parser.add_argument('--ticker', required=True, help='Stock ticker symbol(s), comma-separated for multiple (e.g., AAPL,MSFT,GOOGL)')
    parser.add_argument('--telegram-chat-id', help='Telegram chat ID for posting')
    parser.add_argument('--log-csv', action='store_true', help='Log results to CSV')
    
    args = parser.parse_args()
    logger = setup_logging()
    
    # Split tickers if multiple provided
    tickers = [t.strip() for t in args.ticker.split(',')]
    logger.info(f"Starting market analysis for {len(tickers)} ticker(s): {', '.join(tickers)}")
    
    results = []
    
    for ticker in tickers:
        try:
            logger.info(f"\n--- Analyzing {ticker} ---")
            
            # Fetch ticker data
            logger.info("Fetching ticker data from Yahoo Finance...")
            fetcher = TickerFetcher(ticker)
            ticker_data = fetcher.fetch()
            logger.info(f"Current price: ${ticker_data['current_price']}")
            
            # Calculate SMAs
            logger.info("Calculating simple moving averages...")
            sma_calc = SMACalculator(ticker)
            sma_data = sma_calc.calculate()
            logger.info(f"SMAs calculated - Weekly: {sma_data['sma_weekly']}, "
                       f"Monthly: {sma_data['sma_monthly']}, "
                       f"Quarterly: {sma_data['sma_quarterly']}")
            
            # Fetch news
            logger.info("Fetching news articles...")
            news_fetcher = NewsFetcher(ticker)
            news_articles = news_fetcher.fetch(limit=3)
            logger.info(f"Found {len(news_articles)} news articles")
            
            # Get AI commentary
            logger.info("Generating AI commentary...")
            ai = AICommentary()
            analysis_report = ai.generate_commentary(
                ticker=ticker,
                current_price=ticker_data['current_price'],
                sma_data=sma_data,
                news_articles=news_articles
            )
            logger.info("AI commentary generated")
            
            # Prepare report data
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'ticker': ticker,
                'current_price': ticker_data['current_price'],
                'closing_price': ticker_data.get('closing_price'),
                'sma_weekly': sma_data['sma_weekly'],
                'sma_monthly': sma_data['sma_monthly'],
                'sma_quarterly': sma_data['sma_quarterly'],
                'news_count': len(news_articles),
                'ai_commentary': analysis_report
            }
            
            # Log to CSV
            if args.log_csv:
                logger.info("Logging results to CSV...")
                csv_logger = CSVLogger()
                csv_logger.log_analysis(report_data)
            
            # Post to Telegram
            if args.telegram_chat_id or True:  # Always try to post if available
                logger.info("Posting report to Telegram...")
                telegram = TelegramReporter()
                message = telegram.format_report(
                    ticker=ticker,
                    ticker_data=ticker_data,
                    sma_data=sma_data,
                    news_articles=news_articles,
                    ai_commentary=analysis_report
                )
                telegram.send_message(message, args.telegram_chat_id)
                logger.info("Report posted to Telegram")
            
            results.append({'ticker': ticker, 'status': 'success'})
            logger.info(f"Market analysis for {ticker} completed successfully")
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {str(e)}", exc_info=True)
            results.append({'ticker': ticker, 'status': 'failed', 'error': str(e)})
    
    # Summary
    logger.info(f"\n--- Analysis Summary ---")
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'failed')
    logger.info(f"Completed: {successful}/{len(tickers)} successful")
    if failed > 0:
        logger.warning(f"Failed: {failed} ticker(s)")
    
    # Return 0 if at least one ticker succeeded, 1 only if all failed
    return 0 if successful > 0 else 1


if __name__ == '__main__':
    sys.exit(main())
