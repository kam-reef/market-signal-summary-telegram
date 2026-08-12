"""
Send formatted market analysis reports to Telegram.
"""

import os
import logging
import requests
from typing import Dict, List, Any, Optional


logger = logging.getLogger(__name__)


class TelegramReporter:
    """Send market analysis reports to Telegram."""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.base_url = "https://api.telegram.org/bot"
    
    def send_message(self, message: str, chat_id: Optional[str] = None):
        """
        Send a message to Telegram.
        
        Args:
            message: Message content (supports Markdown formatting)
            chat_id: Telegram chat ID (uses env var if not provided)
        """
        if not self.bot_token:
            logger.warning("TELEGRAM_BOT_TOKEN not set, skipping Telegram post")
            return
        
        if not chat_id:
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not chat_id:
            logger.warning("TELEGRAM_CHAT_ID not set, skipping Telegram post")
            return
        
        try:
            url = f"{self.base_url}{self.bot_token}/sendMessage"
            
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('ok'):
                logger.info(f"Message sent to Telegram chat {chat_id}")
            else:
                logger.warning(f"Telegram API returned: {data.get('description')}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
    
    def format_report(
        self,
        ticker: str,
        ticker_data: Dict[str, Any],
        sma_data: Dict[str, Any],
        news_articles: List[Dict[str, Any]],
        ai_commentary: str
    ) -> str:
        """
        Format analysis data into a readable Telegram message.
        
        Args:
            ticker: Stock ticker symbol
            ticker_data: Ticker data from fetcher
            sma_data: SMA calculations data
            news_articles: List of news articles
            ai_commentary: AI-generated commentary
        
        Returns:
            Formatted message string
        """
        current_price = ticker_data.get('current_price', 0)
        closing_price = ticker_data.get('closing_price', 0)
        pe_ratio = ticker_data.get('pe_ratio')
        
        # Determine signal based on prices vs SMAs
        weekly_pct = sma_data.get('weekly_percent', 0)
        monthly_pct = sma_data.get('monthly_percent', 0)
        
        if weekly_pct > 0 and monthly_pct > 0:
            signal_emoji = "📈"
        elif weekly_pct < 0 and monthly_pct < 0:
            signal_emoji = "📉"
        else:
            signal_emoji = "➡️"
        
        # Build message
        message = f"""
{signal_emoji} *Market Analysis Report* {signal_emoji}

*Ticker:* `{ticker}`

💰 *Price Data*
• Current: ${current_price:.2f}
• Closing: ${closing_price:.2f}
{f'• P/E Ratio: {pe_ratio:.2f}' if pe_ratio else ''}

📊 *Simple Moving Averages (SMA)*
• Weekly (5d): ${sma_data.get('sma_weekly', 0):.2f} ({sma_data.get('weekly_percent', 0):+.2f}%)
• Monthly (21d): ${sma_data.get('sma_monthly', 0):.2f} ({sma_data.get('monthly_percent', 0):+.2f}%)
• Quarterly (63d): ${sma_data.get('sma_quarterly', 0):.2f} ({sma_data.get('quarterly_percent', 0):+.2f}%)

📰 *Latest News*
"""
        
        for i, article in enumerate(news_articles[:3], 1):
            # Create clickable links
            title = article.get('title', 'News')
            url = article.get('url', '#')
            source = article.get('source', 'Unknown')
            message += f"{i}. [{title}]({url})\n   _Source: {source}_\n"
        
        message += f"""
🤖 *AI Analysis*
{ai_commentary}

---
_Report generated via Market Analysis Workflow_
"""
        
        return message
    
    def send_report(
        self,
        ticker: str,
        ticker_data: Dict[str, Any],
        sma_data: Dict[str, Any],
        news_articles: List[Dict[str, Any]],
        ai_commentary: str,
        chat_id: Optional[str] = None
    ):
        """
        Format and send complete report to Telegram.
        
        Args:
            ticker: Stock ticker symbol
            ticker_data: Ticker data from fetcher
            sma_data: SMA calculations data
            news_articles: List of news articles
            ai_commentary: AI-generated commentary
            chat_id: Telegram chat ID (uses env var if not provided)
        """
        message = self.format_report(
            ticker=ticker,
            ticker_data=ticker_data,
            sma_data=sma_data,
            news_articles=news_articles,
            ai_commentary=ai_commentary
        )
        
        self.send_message(message, chat_id)


if __name__ == '__main__':
    # Test
    reporter = TelegramReporter()
    
    ticker_data = {
        'current_price': 153.50,
        'closing_price': 152.80,
        'pe_ratio': 28.5
    }
    
    sma_data = {
        'sma_weekly': 151.20,
        'sma_monthly': 150.50,
        'sma_quarterly': 148.00,
        'weekly_percent': 1.52,
        'monthly_percent': 1.99,
        'quarterly_percent': 3.65
    }
    
    news_articles = [
        {
            'title': 'Apple Reports Strong Q4 Earnings',
            'url': 'https://example.com/apple-earnings',
            'source': 'Financial Times'
        }
    ]
    
    message = reporter.format_report(
        'AAPL',
        ticker_data,
        sma_data,
        news_articles,
        'Stock is in an uptrend with positive momentum.'
    )
    
    print(message)
