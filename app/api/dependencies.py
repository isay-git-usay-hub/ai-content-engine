from fastapi import Depends, HTTPException
from app.ai.analyzer import AIAnalyzer
from app.collectors import GoogleTrendsCollector, RedditCollector, NewsAPICollector
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache()
def get_ai_analyzer() -> AIAnalyzer:
    """Dependency to get Gemini AI analyzer instance"""
    try:
        return AIAnalyzer()
    except Exception as e:
        logger.error(f"Failed to initialize Gemini analyzer: {e}")
        raise HTTPException(status_code=500, detail=f"AI service unavailable: {str(e)}")

class CollectorManager:
    def __init__(self):
        self.collectors = {
            'google_trends': GoogleTrendsCollector(),
            'reddit': RedditCollector(),
            'news': NewsAPICollector(),
        }
    
    def get_collector(self, platform: str):
        """Get specific platform collector"""
        if platform not in self.collectors:
            raise HTTPException(
                status_code=404, 
                detail=f"Collector for platform '{platform}' not found"
            )
        return self.collectors[platform]
    
    def get_all_collectors(self):
        """Get all available collectors"""
        return self.collectors

@lru_cache()
def get_collector_manager() -> CollectorManager:
    """Dependency to get collector manager instance"""
    return CollectorManager()
