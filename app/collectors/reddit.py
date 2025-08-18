from typing import List, Dict, Any
import logging
import aiohttp
from .base import BaseCollector
from app.config import settings

logger = logging.getLogger(__name__)

class RedditCollector(BaseCollector):
    def __init__(self, limit: int = 10):
        super().__init__(limit)
        self.headers = {'User-agent': getattr(settings, 'REDDIT_USER_AGENT', 'AIContentEngine/1.0')}

    async def collect(self) -> List[Dict[str, Any]]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'https://www.reddit.com/r/all/hot.json?limit={self.limit}',
                    headers=self.headers
                ) as response:
                    data = await response.json()
                    
                    posts = data['data']['children']
                    formatted_data = [
                        {
                            'title': post['data']['title'],
                            'platform': 'reddit',
                            'engagement_score': post['data']['score'],
                            'url': f"https://reddit.com{post['data']['permalink']}",
                            'metadata': {
                                'subreddit': post['data']['subreddit'],
                                'comments': post['data']['num_comments'],
                                'upvote_ratio': post['data'].get('upvote_ratio', 0)
                            }
                        }
                        for post in posts
                    ]
                    
                    return self.validate_data(formatted_data)
                    
        except Exception as e:
            logger.error(f"Error collecting Reddit trends: {str(e)}")
            raise  # ← NO FALLBACK - Fail honestly
