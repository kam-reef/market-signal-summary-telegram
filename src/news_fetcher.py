"""
Fetch news articles related to a stock ticker using NewsAPI.
"""

import os
import logging
import requests
from typing import List, Dict, Any


logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetch news articles from NewsAPI."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    def fetch(self, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Fetch news articles related to the ticker.
        
        Args:
            limit: Maximum number of articles to fetch
        
        Returns:
            List of news articles
        """
        if not self.api_key:
            logger.warning("NEWS_API_KEY not set, returning mock news")
            return self._generate_mock_news()
        
        try:
            url = f"{self.base_url}/everything"
            
            params = {
                'q': self.ticker,
                'sortBy': 'publishedAt',
                'language': 'en',
                'apiKey': self.api_key,
                'pageSize': limit * 2  # Fetch extra to filter quality
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                logger.warning(f"NewsAPI returned status: {data.get('status')}")
                return self._generate_mock_news()
            
            articles = data.get('articles', [])
            
            # Filter and limit articles
            filtered_articles = []
            for article in articles[:limit * 2]:
                if article.get('url') and article.get('title'):
                    filtered_articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'published_at': article.get('publishedAt'),
                        'description': article.get('description', ''),
                    })
                if len(filtered_articles) >= limit:
                    break
            
            logger.info(f"Fetched {len(filtered_articles)} news articles for {self.ticker}")
            return filtered_articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news: {str(e)}")
            return self._generate_mock_news()
    
    def _generate_mock_news(self) -> List[Dict[str, Any]]:
        """Generate mock news articles for demonstration."""
        return [
            {
                'title': f'{self.ticker} Shows Strong Performance in Q3',
                'url': f'https://example.com/news/{self.ticker.lower()}-q3',
                'source': 'Market News Today',
                'published_at': '2024-01-15T10:00:00Z',
                'description': 'The company reported strong earnings and positive outlook.'
            },
            {
                'title': f'Analyst Upgrades {self.ticker} Rating',
                'url': f'https://example.com/news/{self.ticker.lower()}-upgrade',
                'source': 'Financial Times',
                'published_at': '2024-01-14T15:30:00Z',
                'description': 'Leading analyst upgraded the stock to Buy rating.'
            },
            {
                'title': f'{self.ticker} Launches New Product Line',
                'url': f'https://example.com/news/{self.ticker.lower()}-product',
                'source': 'TechNews',
                'published_at': '2024-01-13T12:00:00Z',
                'description': 'The company announced an innovative product launch.'
            }
        ]


if __name__ == '__main__':
    # Test
    fetcher = NewsFetcher('AAPL')
    news = fetcher.fetch(limit=3)
    for article in news:
        print(f"- {article['title']}")
        print(f"  {article['url']}\n")
