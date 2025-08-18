from typing import List, Dict, Any
import logging
import random
import aiohttp
from .base import BaseCollector

logger = logging.getLogger(__name__)

class NewsAPICollector(BaseCollector):
    """Free news collector using RSS feeds and mock data as fallback"""
    
    def __init__(self, limit: int = 10):
        super().__init__(limit)
        self.rss_feeds = [
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.cnn.com/rss/edition.rss",
            "https://feeds.reuters.com/reuters/topNews",
            "https://feeds.npr.org/1001/rss.xml"
        ]
    
    async def collect(self) -> List[Dict[str, Any]]:
        try:
            # Try to fetch from RSS feeds
            async with aiohttp.ClientSession() as session:
                all_news = []
                for feed_url in self.rss_feeds:
                    try:
                        async with session.get(feed_url, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                # Simple RSS parsing - extract titles and links
                                import xml.etree.ElementTree as ET
                                root = ET.fromstring(content)
                                items = root.findall('.//item')
                                
                                for item in items[:3]:  # Take 3 from each feed
                                    title_elem = item.find('title')
                                    link_elem = item.find('link')
                                    
                                    if title_elem is not None and link_elem is not None:
                                        all_news.append({
                                            'title': title_elem.text,
                                            'platform': 'news',
                                            'engagement_score': random.randint(500, 2000),
                                            'url': link_elem.text,
                                            'metadata': {
                                                'source': feed_url.split('/')[2],
                                                'type': 'news_article',
                                                'published': item.find('pubDate').text if item.find('pubDate') is not None else None
                                            }
                                        })
                                
                                if len(all_news) >= self.limit:
                                    break
                    except Exception as e:
                        logger.warning(f"Failed to fetch from {feed_url}: {str(e)}")
                        continue
                
                if all_news:
                    return self.validate_data(all_news[:self.limit])
                
        except Exception as e:
            logger.error(f"Error collecting news data: {str(e)}")
        
        logger.info("Falling back to mock news data")
        return self._get_mock_news_data()
    
    def _get_mock_news_data(self) -> List[Dict[str, Any]]:
        """Provide mock news data when RSS feeds fail"""
        mock_news = [
            {
                'title': 'AI Revolution: How Machine Learning is Transforming Content Creation',
                'platform': 'news',
                'engagement_score': 1850,
                'url': 'https://example.com/ai-content-creation',
                'metadata': {
                    'source': 'TechNewsDaily',
                    'type': 'technology',
                    'published': '2024-01-15T12:00:00Z',
                    'source': 'mock_data'
                }
            },
            {
                'title': 'Remote Work Trends 2024: Companies Embrace Hybrid Models',
                'platform': 'news',
                'engagement_score': 1420,
                'url': 'https://example.com/remote-work-trends',
                'metadata': {
                    'source': 'BusinessWeekly',
                    'type': 'business',
                    'published': '2024-01-15T11:30:00Z',
                    'source': 'mock_data'
                }
            },
            {
                'title': 'Gen Z Mental Health Crisis: New Study Reveals Alarming Statistics',
                'platform': 'news',
                'engagement_score': 2300,
                'url': 'https://example.com/gen-z-mental-health',
                'metadata': {
                    'source': 'HealthJournal',
                    'type': 'health',
                    'published': '2024-01-15T10:15:00Z',
                    'source': 'mock_data'
                }
            },
            {
                'title': 'Cryptocurrency Market Sees Surge as Bitcoin Hits New Highs',
                'platform': 'news',
                'engagement_score': 1680,
                'url': 'https://example.com/crypto-surge',
                'metadata': {
                    'source': 'FinanceToday',
                    'type': 'finance',
                    'published': '2024-01-15T09:45:00Z',
                    'source': 'mock_data'
                }
            },
            {
                'title': 'Climate Change Solutions: Tech Giants Lead Sustainability Efforts',
                'platform': 'news',
                'engagement_score': 1950,
                'url': 'https://example.com/climate-tech',
                'metadata': {
                    'source': 'EcoWatch',
                    'type': 'environment',
                    'published': '2024-01-15T08:30:00Z',
                    'source': 'mock_data'
                }
            }
        ]
        
        # Randomly select and shuffle mock news
        selected_news = random.sample(mock_news, min(self.limit, len(mock_news)))
        random.shuffle(selected_news)
        
        # Add some variation to engagement scores
        for news in selected_news:
            news['engagement_score'] += random.randint(-200, 200)
        
        return self.validate_data(selected_news)