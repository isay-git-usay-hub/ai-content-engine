from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class TrendItem(BaseModel):
    title: str
    platform: str
    engagement_score: Optional[int] = None
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class TrendingData(BaseModel):
    google_trends: List[Dict[str, Any]]  # ← Fixed: Changed from List[str] to List[Dict[str, Any]]
    reddit_trends: List[Dict[str, Any]]
    news_trends: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ContentRecommendation(BaseModel):
    title: str
    format: str  # "Reel", "Short", "Post", "Story"
    platform: str
    best_time: str
    hook: str
    description: str

class StrategyResponse(BaseModel):
    top_trends: List[TrendItem]
    content_strategy: List[ContentRecommendation]
    analysis_summary: str
    generated_at: datetime = Field(default_factory=datetime.now)

class AnalysisRequest(BaseModel):
    trends_data: TrendingData
    target_audience: Optional[str] = "Gen Z"
    niche: Optional[str] = "General"
    days: Optional[int] = 7

class CompetitorData(BaseModel):
    username: str
    platform: str
    follower_count: int
    post_frequency: str
    avg_engagement: float
    top_topics: List[str]
    content_formats: List[str]
    recent_posts: List[Dict[str, Any]]
    analysis_date: datetime = Field(default_factory=datetime.now)

class CompetitorAnalysis(BaseModel):
    competitors: List[CompetitorData]
    competitive_insights: Dict[str, Any]
    gap_opportunities: List[str]
    benchmark_recommendations: List[str]
    analysis_date: datetime = Field(default_factory=datetime.now)
