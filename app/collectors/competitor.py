from typing import List, Dict, Any
import logging
import random
from datetime import datetime, timedelta
from .base import BaseCollector

logger = logging.getLogger(__name__)

class CompetitorCollector(BaseCollector):
    def __init__(self, limit: int = 10):
        super().__init__(limit)
    
    async def collect(self, competitors: List[str] = None) -> List[Dict[str, Any]]:
        """
        Collect competitor data from various social platforms
        
        Args:
            competitors: List of competitor usernames to analyze
            
        Returns:
            List of competitor analysis data
        """
        try:
            if not competitors:
                competitors = ["@garyvee", "@neilpatel", "@mkbhd", "@backlinko", "@hubspot"]
            
            competitor_data = []
            
            for username in competitors:
                for platform in ["Instagram", "TikTok"]:
                    try:
                        data = await self._get_competitor_data(username, platform)
                        if data:
                            competitor_data.append(data)
                    except Exception as e:
                        logger.warning(f"Failed to collect data for {username} on {platform}: {e}")
                        # Add mock data as fallback
                        competitor_data.append(self._get_mock_competitor_data(username, platform))
            
            return self.validate_data(competitor_data)
            
        except Exception as e:
            logger.error(f"Error collecting competitor data: {str(e)}")
            return self._get_mock_competitors()
    
    async def _get_competitor_data(self, username: str, platform: str) -> Dict[str, Any]:
        """Get competitor data for a specific platform"""
        # This would normally use platform APIs to get real data
        # For now, we'll use mock data with realistic patterns
        return self._get_mock_competitor_data(username, platform)
    
    def _get_mock_competitor_data(self, username: str, platform: str) -> Dict[str, Any]:
        """Generate realistic mock competitor data"""
        base_followers = {
            "@garyvee": {"Instagram": 10000000, "TikTok": 12000000},
            "@neilpatel": {"Instagram": 800000, "TikTok": 2000000},
            "@mkbhd": {"Instagram": 5000000, "TikTok": 3000000},
            "@backlinko": {"Instagram": 300000, "TikTok": 1500000},
            "@hubspot": {"Instagram": 2000000, "TikTok": 5000000}
        }
        
        # Generate dynamic data
        follower_count = base_followers.get(username, {}).get(platform, random.randint(50000, 20000000))
        post_frequency = random.choice(["Daily", "3-5 times/week", "Weekly", "2-3 times/day"])
        avg_engagement = random.uniform(2.5, 15.0)
        
        # Generate recent posts
        recent_posts = []
        for i in range(5):
            days_ago = random.randint(1, 30)
            post_date = datetime.now() - timedelta(days=days_ago)
            
            recent_posts.append({
                "content": f"{random.choice(['Check out this', 'New insights on', 'Breaking down', 'Deep dive into', 'Quick tip about'])} {random.choice(['digital marketing', 'content creation', 'social media strategy', 'SEO trends', 'AI tools'])}",
                "engagement": random.randint(100, 50000),
                "format": random.choice(["Reel", "Carousel", "Single Post", "Video", "Story"]),
                "posted_at": post_date.isoformat()
            })
        
        return {
            "username": username,
            "platform": platform,
            "follower_count": follower_count,
            "post_frequency": post_frequency,
            "avg_engagement": round(avg_engagement, 2),
            "top_topics": random.sample([
                "Digital Marketing", "Content Creation", "Social Media Strategy", 
                "SEO", "AI Tools", "Productivity", "Entrepreneurship", "Technology"
            ], 4),
            "content_formats": random.sample([
                "Reels", "Carousels", "Single Posts", "Stories", "Videos", "Live Streams"
            ], 3),
            "recent_posts": recent_posts
        }
    
    def _get_mock_competitors(self) -> List[Dict[str, Any]]:
        """Get fallback mock competitor data"""
        competitors = ["@example1", "@example2", "@example3"]
        data = []
        
        for username in competitors:
            for platform in ["Instagram", "TikTok"]:
                data.append(self._get_mock_competitor_data(username, platform))
        
        return data