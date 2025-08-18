from fastapi import APIRouter, HTTPException, Depends
from app.models import TrendingData, StrategyResponse, AnalysisRequest
from app.collectors.reddit import RedditCollector
from app.collectors.google_trends import GoogleTrendsCollector
from app.collectors.competitor import CompetitorCollector
from app.ai.analyzer import AIAnalyzer
from datetime import datetime, timedelta
import asyncio
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
router = APIRouter()

# Cache to prevent repeated API calls
cache = {
    "trending_data": None,
    "last_update": None,
    "cache_duration": timedelta(minutes=15)
}  # ← Fixed: Added missing closing bracket

def get_ai_analyzer():
    return AIAnalyzer()

@router.get("/trending", response_model=TrendingData)
async def get_trending_data():
    """Collect REAL trending data from APIs only"""
    try:
        # Check cache first
        now = datetime.now()
        if (cache["trending_data"] and cache["last_update"] and 
            now - cache["last_update"] < cache["cache_duration"]):
            logger.info("📋 Returning cached trending data")
            return cache["trending_data"]

        logger.info("🔄 Collecting fresh trending data from real APIs")

        # Initialize collectors
        google_collector = GoogleTrendsCollector()
        reddit_collector = RedditCollector()

        # Collect from real APIs with timeout
        google_trends = []
        reddit_trends = []

        try:
            # Google Trends with timeout
            google_trends = await asyncio.wait_for(
                google_collector.collect(), 
                timeout=15.0
            )  # ← Fixed: Added missing closing bracket
            logger.info(f"✅ Google Trends: collected {len(google_trends)} trends")
        except asyncio.TimeoutError:
            logger.warning("⏰ Google Trends timed out")
        except Exception as e:
            logger.warning(f"❌ Google Trends failed: {str(e)}")

        try:
            # Reddit with timeout
            reddit_trends = await asyncio.wait_for(
                reddit_collector.collect(), 
                timeout=10.0
            )  # ← Fixed: Added missing closing bracket
            logger.info(f"✅ Reddit: collected {len(reddit_trends)} trends")
        except asyncio.TimeoutError:
            logger.warning("⏰ Reddit timed out")
        except Exception as e:
            logger.warning(f"❌ Reddit failed: {str(e)}")

        # Check if we got any real data
        if not google_trends and not reddit_trends:
            raise HTTPException(
                status_code=503, 
                detail="No trending data available from any real API source"
            )  # ← Fixed: Added missing closing bracket

        # Create response with only real API data
        trending_data = TrendingData(
            google_trends=google_trends,  # ← Now passes full objects
            reddit_trends=reddit_trends,
            timestamp=now
        )  # ← Fixed: Added missing closing bracket

        # Cache the real result
        cache["trending_data"] = trending_data
        cache["last_update"] = now

        logger.info("✅ Real data collected and cached")
        return trending_data

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"❌ Data collection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

@router.post("/analyze", response_model=StrategyResponse)
async def analyze_trends(
    request: AnalysisRequest,
    analyzer: AIAnalyzer = Depends(get_ai_analyzer)
):
    """Analyze real trends and generate content strategy"""
    try:
        logger.info(f"🧠 Analyzing real trends for {request.target_audience} in {request.niche}")
        
        strategy = await analyzer.analyze_trends(
            request.trends_data,
            request.target_audience,
            request.niche
        )  # ← Fixed: Added missing closing bracket
        
        logger.info("✅ Real trend analysis completed")
        return strategy
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/strategy", response_model=StrategyResponse)
async def get_complete_strategy(
    target_audience: str = "Gen Z",
    niche: str = "General",
    analyzer: AIAnalyzer = Depends(get_ai_analyzer)
):
    """Complete workflow with REAL data only"""
    try:
        logger.info(f"🎯 Generating strategy from real data for {target_audience} in {niche}")
        
        # Get real trending data (will fail if no real APIs work)
        trending_data = await get_trending_data()
        
        # Generate strategy with AI using real data
        strategy = await analyzer.analyze_trends(trending_data, target_audience, niche)
        
        logger.info("✅ Real data strategy generated successfully")
        return strategy
        
    except Exception as e:
        logger.error(f"❌ Strategy generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Strategy generation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check - shows real API status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_status": "cached" if cache["trending_data"] else "empty",
        "last_update": cache["last_update"].isoformat() if cache["last_update"] else None,
        "data_source": "real_apis_only"
    }

@router.get("/cache/clear")
async def clear_cache():
    """Clear cache to force fresh API calls"""
    cache["trending_data"] = None
    cache["last_update"] = None
    logger.info("🗑️ Cache cleared - next request will hit real APIs")
    return {"message": "Cache cleared - next request will fetch fresh data from real APIs"}

@router.get("/test")
async def test_real_apis():
    """Test real API connections only"""
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "testing": "real_apis_only"
    }

    # Test Google Trends
    try:
        google_collector = GoogleTrendsCollector()
        google_data = await asyncio.wait_for(google_collector.collect(), timeout=10.0)
        test_results["google_trends"] = {
            "status": "✅ Working",
            "count": len(google_data),
            "sample": google_data[0] if google_data else None
        }
    except Exception as e:
        test_results["google_trends"] = {
            "status": f"❌ Failed: {str(e)}"
        }

    # Test Reddit
    try:
        reddit_collector = RedditCollector()
        reddit_data = await asyncio.wait_for(reddit_collector.collect(), timeout=10.0)
        test_results["reddit"] = {
            "status": "✅ Working",
            "count": len(reddit_data),
            "sample": reddit_data[0] if reddit_data else None
        }
    except Exception as e:
        test_results["reddit"] = {
            "status": f"❌ Failed: {str(e)}"
        }

    # Test AI Analyzer
    try:
        analyzer = AIAnalyzer()
        test_results["ai_analyzer"] = "✅ Initialized"
    except Exception as e:
        test_results["ai_analyzer"] = f"❌ Failed: {str(e)}"

@router.post("/competitors", response_model=List[Dict[str, Any]])
async def get_competitor_data(request: AnalysisRequest):
    """Collect competitor data"""
    try:
        collector = CompetitorCollector()
        competitor_data = await collector.collect(request.competitors)
        return competitor_data
    except Exception as e:
        logger.error(f"❌ Competitor data collection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Competitor data collection failed: {str(e)}")

    return test_results
