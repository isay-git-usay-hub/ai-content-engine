from typing import List, Dict, Any
import logging
from .base import BaseCollector
from .reddit import RedditCollector
import asyncio

logger = logging.getLogger(__name__)

try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False
    logger.warning("pytrends not available, using mock data for Google Trends")

logger = logging.getLogger(__name__)

class GoogleTrendsCollector(BaseCollector):
    def __init__(self, limit: int = 10):
        super().__init__(limit)
        self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25)) if PYTRENDS_AVAILABLE else None

    async def collect(self, country: str = 'india') -> List[Dict[str, Any]]:
        """
        Collects trending searches from Google Trends for a specific country.
        Does not fall back to other collectors on failure.
        """
        if not PYTRENDS_AVAILABLE or not self.pytrends:
            logger.warning("pytrends library not available, returning empty list for Google Trends.")
            return []
            
        try:
            loop = asyncio.get_event_loop()
            
            def get_trends_sync():
                # Use the country parameter for targeted trend collection
                trending_df = self.pytrends.trending_searches(pn=country)
                return trending_df.head(self.limit).values.flatten().tolist()
            
            trends_list = await loop.run_in_executor(None, get_trends_sync)
            
            formatted_data = [
                {
                    'title': trend,
                    'platform': 'google_trends',
                    'engagement_score': max(1000 - (i * 100), 100),
                    'url': f"https://trends.google.com/trends/explore?q={trend.replace(' ', '+')}",
                    'metadata': {
                        'type': 'trending_search',
                        'rank': i + 1,
                        'region': country
                    }
                }
                for i, trend in enumerate(trends_list)
            ]
            
            return self.validate_data(formatted_data)
            
        except Exception as e:
            logger.error(f"Error collecting Google Trends for country '{country}': {str(e)}")
            logger.warning(f"Could not fetch data from Google Trends, returning empty list.")
            return []
