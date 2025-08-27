import pytest
from unittest.mock import MagicMock, AsyncMock
import pandas as pd
from app.collectors.google_trends import GoogleTrendsCollector
from app.collectors.reddit import RedditCollector

@pytest.mark.asyncio
async def test_google_trends_collector(mocker):
    """Test the Google Trends collector with a mocked API call."""
    # Mock the pytrends library to avoid real API calls
    mock_df = pd.DataFrame(['Trend 1', 'Trend 2', 'Trend 3'])

    mock_pytrends_instance = MagicMock()
    mock_pytrends_instance.trending_searches.return_value = mock_df
    mocker.patch('app.collectors.google_trends.TrendReq', return_value=mock_pytrends_instance)

    collector = GoogleTrendsCollector(limit=3)
    data = await collector.collect()
    
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]['title'] == 'Trend 1'
    assert data[0]['platform'] == 'google_trends'

@pytest.mark.asyncio
async def test_reddit_collector(mocker):
    """Test the Reddit collector with a mocked API call."""
    # The mock JSON response we expect from Reddit
    mock_json_response = {
        'data': {
            'children': [
                {'data': {'title': 'Reddit Post 1', 'score': 100, 'permalink': '/r/test/post1', 'subreddit': 'test', 'num_comments': 10, 'upvote_ratio': 0.9}},
                {'data': {'title': 'Reddit Post 2', 'score': 200, 'permalink': '/r/test/post2', 'subreddit': 'test', 'num_comments': 20, 'upvote_ratio': 0.8}},
            ]
        }
    }

    # Mock the response object that the context manager will yield
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_json_response)

    # Mock the async context manager that `session.get` returns
    async_context_manager = AsyncMock()
    async_context_manager.__aenter__.return_value = mock_response

    # Patch the `get` method of aiohttp.ClientSession
    mocker.patch('aiohttp.ClientSession.get', return_value=async_context_manager)

    collector = RedditCollector(limit=2)
    data = await collector.collect()
    
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['title'] == 'Reddit Post 1'
    assert data[0]['platform'] == 'reddit'
    assert data[1]['engagement_score'] == 200
    assert data[1]['metadata']['subreddit'] == 'test'
