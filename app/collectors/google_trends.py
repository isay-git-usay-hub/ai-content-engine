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

    async def collect(self) -> List[Dict[str, Any]]:
        if not PYTRENDS_AVAILABLE or not self.pytrends:
            logger.info("Using Reddit data (pytrends unavailable)")
            return await RedditCollector(self.limit).collect()
            
        try:
            loop = asyncio.get_event_loop()
            
            def get_trends():
                trending = self.pytrends.trending_searches(pn='india')
                return trending.head(self.limit).values.flatten().tolist()
            
            trends_list = await loop.run_in_executor(None, get_trends)
            
            # Generate dynamic engagement scores based on trend position
            formatted_data = [
                {
                    'title': trend,
                    'platform': 'google_trends',
                    'engagement_score': max(1000 - (i * 100), 100),  # Higher score for top trends
                    'url': f"https://trends.google.com/trends/explore?q={trend}",
                    'metadata': {
                        'type': 'trending_search',
                        'rank': i + 1,
                        'region': 'india'
                    }
                }
                for i, trend in enumerate(trends_list)
            ]
            
            return self.validate_data(formatted_data)
            
        except Exception as e:
            logger.error(f"Error collecting Google Trends: {str(e)}")
            logger.info("Falling back to Reddit data due to API issues")
            return await RedditCollector(self.limit).collect()
