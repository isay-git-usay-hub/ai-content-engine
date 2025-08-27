import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from app.ai.analyzer import AIAnalyzer
from app.collectors.google_trends import GoogleTrendsCollector
from app.collectors.reddit import RedditCollector
from app.models import TrendingData, StrategyResponse

logger = logging.getLogger(__name__)

# In-memory cache
cache = {
    "trending_data": None,
    "last_update": None,
    "cache_duration": timedelta(minutes=15)
}

async def get_trends() -> Optional[TrendingData]:
    """
    Collects trending data from Google Trends and Reddit with caching.
    This is a refactored, UI-agnostic version of the original FastAPI endpoint.
    """
    now = datetime.now()
    if (cache["trending_data"] and cache["last_update"] and
            now - cache["last_update"] < cache["cache_duration"]):
        logger.info("📋 Returning cached trending data")
        return cache["trending_data"]

    logger.info("🔄 Collecting fresh trending data...")

    google_collector = GoogleTrendsCollector()
    reddit_collector = RedditCollector()

    google_trends, reddit_trends = [], []

    # Await collectors concurrently
    results = await asyncio.gather(
        google_collector.collect(),
        reddit_collector.collect(),
        return_exceptions=True
    )

    if isinstance(results[0], list):
        google_trends = results[0]
        logger.info(f"✅ Google Trends: collected {len(google_trends)} trends")
    else:
        logger.warning(f"❌ Google Trends failed: {results[0]}")

    if isinstance(results[1], list):
        reddit_trends = results[1]
        logger.info(f"✅ Reddit: collected {len(reddit_trends)} trends")
    else:
        logger.warning(f"❌ Reddit failed: {results[1]}")

    if not google_trends and not reddit_trends:
        logger.error("No trending data available from any source.")
        return None

    trending_data = TrendingData(
        google_trends=google_trends,
        reddit_trends=reddit_trends,
        timestamp=now
    )

    # Cache the result
    cache["trending_data"] = trending_data
    cache["last_update"] = now

    logger.info("✅ Data collected and cached")
    return trending_data

async def generate_strategy(target_audience: str, niche: str) -> Optional[StrategyResponse]:
    """
    Generates a complete content strategy by fetching trends and analyzing them.
    """
    logger.info(f"🎯 Generating strategy for {target_audience} in {niche}")

    trending_data = await get_trends()
    if not trending_data:
        logger.error("Cannot generate strategy without trending data.")
        return None

    try:
        analyzer = AIAnalyzer()
        strategy = await analyzer.analyze_trends(trending_data, target_audience, niche)
        logger.info("✅ Strategy generated successfully")
        return strategy
    except Exception as e:
        logger.error(f"❌ Strategy generation failed: {e}")
        return None

from app.collectors.competitor import CompetitorCollector
from typing import List, Dict, Any

def clear_trends_cache():
    """Clears the in-memory cache for trending data."""
    global cache
    cache["trending_data"] = None
    cache["last_update"] = None
    logger.info("🗑️ Trends cache cleared.")

async def fetch_competitor_data(competitors: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Collects competitor data.
    """
    logger.info(f"Collecting competitor data for: {competitors or 'default competitors'}")
    try:
        collector = CompetitorCollector()
        data = await collector.collect(competitors=competitors)
        logger.info(f"Successfully collected data for {len(data)} competitor profiles.")
        return data
    except Exception as e:
        logger.error(f"❌ Competitor data collection failed: {e}")
        return []
