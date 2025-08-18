from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class StrategyGenerator:
    def __init__(self):
        self.content_formats = [
            "Reel", "Short", "Post", "Story", "Carousel", "IGTV", "Thread"
        ]  # ← Fixed: Added missing closing bracket

        self.posting_times = [
            "6:00 AM", "9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM", "9:00 PM"
        ]  # ← Fixed: Added missing closing bracket

        self.engagement_hooks = [
            "Challenge", "Tutorial", "Behind-the-scenes", "Tips", "Story", "Trend"
        ]  # ← Fixed: Added missing closing bracket

    def generate_30_day_calendar(self, top_trends: List[Dict], target_audience: str = "Gen Z") -> List[Dict]:
        """Generate a 30-day content calendar based on trends"""
        if not top_trends:
            raise ValueError("No trends provided for calendar generation")
            
        calendar = []
        start_date = datetime.now()

        for day in range(30):
            current_date = start_date + timedelta(days=day)

            # Cycle through trends to ensure variety
            trend = top_trends[day % len(top_trends)]

            content_item = {
                "date": current_date.strftime("%Y-%m-%d"),
                "title": f"{trend['title']} - {target_audience} Edition",
                "format": self.content_formats[day % len(self.content_formats)],
                "platform": self._recommend_platform(trend['platform']),
                "best_time": self.posting_times[day % len(self.posting_times)],
                "hook": self.engagement_hooks[day % len(self.engagement_hooks)],
                "description": f"Create content around {trend['title']} targeting {target_audience}",
                "hashtags": self._generate_hashtags(trend['title']),
                "cta": self._generate_cta(trend['title'])
            }  # ← Fixed: Added missing closing bracket

            calendar.append(content_item)

        return calendar

    def _recommend_platform(self, source_platform: str) -> str:
        """Recommend best platform based on trend source"""
        platform_mapping = {
            "google_trends": "Instagram",
            "reddit": "TikTok"
        }  # ← Fixed: Added missing closing bracket
        return platform_mapping.get(source_platform, "Instagram")

    def _generate_hashtags(self, title: str) -> List[str]:
        """Generate relevant hashtags"""
        words = title.lower().split()
        hashtags = [f"#{word}" for word in words if len(word) > 3]
        hashtags.extend(["#trending", "#viral", "#content"])
        return hashtags[:10]  # Limit to 10 hashtags

    def _generate_cta(self, title: str) -> str:
        """Generate call-to-action"""
        ctas = [
            "Double tap if you agree! 💙",
            "Save this for later! 📌",
            "Share your thoughts below! 👇",
            "Tag someone who needs this! 🔥",
            "Follow for more trending content! ✨"
        ]  # ← Fixed: Added missing closing bracket
        return ctas[hash(title) % len(ctas)]
