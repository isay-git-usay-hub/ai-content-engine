import pytest
from app.collectors.google_trends import GoogleTrendsCollector
from app.collectors.reddit import RedditCollector

@pytest.mark.asyncio
async def test_google_trends_collector():
    collector = GoogleTrendsCollector(limit=5)
    data = await collector.collect()
    
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        assert 'title' in data[0]
        assert 'platform' in data[0]

@pytest.mark.asyncio
async def test_reddit_collector():
    collector = RedditCollector(limit=5)
    data = await collector.collect()
    
    assert isinstance(data, list)
    if data:
        assert 'title' in data[0]
        assert 'engagement_score' in data[0]
