"""
Generate AI-powered commentary using OpenRouter API.
"""

import os
import logging
import requests
import json
from typing import Dict, List, Any


logger = logging.getLogger(__name__)


class AICommentary:
    """Generate AI commentary using OpenRouter."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "openrouter/free"  # Free tier model
    
    def generate_commentary(
        self,
        ticker: str,
        current_price: float,
        sma_data: Dict[str, Any],
        news_articles: List[Dict[str, Any]]
    ) -> str:
        """
        Generate AI commentary on stock analysis.
        
        Args:
            ticker: Stock ticker symbol
            current_price: Current stock price
            sma_data: SMA calculations data
            news_articles: List of relevant news articles
        
        Returns:
            AI-generated commentary string
        """
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set, using mock commentary")
            return self._generate_mock_commentary(ticker, current_price, sma_data)
        
        try:
            # Prepare the prompt
            prompt = self._build_prompt(ticker, current_price, sma_data, news_articles)
            
            # Call OpenRouter API
            url = f"{self.base_url}/chat/completions"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://github.com/market-analysis-workflow',
                'X-Title': 'Market Analysis Workflow'
            }
            
            payload = {
                'model': 'mistralai/mistral-7b-instruct:free',
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 500
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                commentary = data['choices'][0]['message']['content']
                logger.info("AI commentary generated successfully")
                return commentary
            else:
                logger.warning("Unexpected response format from OpenRouter")
                return self._generate_mock_commentary(ticker, current_price, sma_data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling OpenRouter API: {str(e)}")
            return self._generate_mock_commentary(ticker, current_price, sma_data)
    
    def _build_prompt(
        self,
        ticker: str,
        current_price: float,
        sma_data: Dict[str, Any],
        news_articles: List[Dict[str, Any]]
    ) -> str:
        """Build the prompt for AI commentary."""
        news_summary = "\n".join([
            f"- {article['title']}"
            for article in news_articles[:3]
        ])
        
        prompt = f"""Analyze the following stock data and provide a brief, actionable commentary for investment decision-making.

Stock: {ticker}
Current Price: ${current_price}

Simple Moving Averages:
- Weekly SMA: ${sma_data.get('sma_weekly')} (Change: {sma_data.get('weekly_percent')}%)
- Monthly SMA: ${sma_data.get('sma_monthly')} (Change: {sma_data.get('monthly_percent')}%)
- Quarterly SMA: ${sma_data.get('sma_quarterly')} (Change: {sma_data.get('quarterly_percent')}%)

Recent News:
{news_summary}

Provide a 2-3 sentence analysis considering:
1. Price position relative to moving averages
2. Recent news sentiment
3. Overall market signal (Bullish/Neutral/Bearish)

Format: Brief insight | Signal | Recommendation"""
        
        return prompt
    
    def _generate_mock_commentary(
        self,
        ticker: str,
        current_price: float,
        sma_data: Dict[str, Any]
    ) -> str:
        """Generate mock commentary for demonstration."""
        weekly_pct = sma_data.get('weekly_percent', 0)
        monthly_pct = sma_data.get('monthly_percent', 0)
        
        if weekly_pct > 2 and monthly_pct > 2:
            signal = "BULLISH"
            recommendation = "HOLD/BUY"
            insight = f"{ticker} is trading above all major moving averages, indicating uptrend strength."
        elif weekly_pct < -2 and monthly_pct < -2:
            signal = "BEARISH"
            recommendation = "SELL/HOLD"
            insight = f"{ticker} is trading below major moving averages, suggesting caution."
        else:
            signal = "NEUTRAL"
            recommendation = "HOLD"
            insight = f"{ticker} is consolidating around key moving average levels."
        
        return f"{insight} | Signal: {signal} | Recommendation: {recommendation}"


if __name__ == '__main__':
    # Test
    ai = AICommentary()
    sma_data = {
        'sma_weekly': 150.0,
        'sma_monthly': 148.0,
        'sma_quarterly': 145.0,
        'weekly_percent': 2.5,
        'monthly_percent': 3.0,
        'quarterly_percent': 4.0
    }
    news = [
        {'title': 'Stock rises on earnings beat'},
        {'title': 'Analyst upgrades stock'},
        {'title': 'Company announces new product'}
    ]
    commentary = ai.generate_commentary('AAPL', 153.5, sma_data, news)
    print(commentary)
