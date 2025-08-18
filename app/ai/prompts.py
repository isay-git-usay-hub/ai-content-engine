ANALYSIS_PROMPT = """
Analyze these trending topics and generate a content strategy:

TRENDING DATA:
{trends_data}

TARGET AUDIENCE: {target_audience}
NICHE: {niche}

Tasks:
1. Identify the TOP 10 most engaging trends across all platforms
2. Analyze success factors (format, tone, timing, engagement drivers)
3. Generate 7-day content strategy with specific recommendations

Return ONLY valid JSON with this structure:
{{
  "top_trends": [
    {{
      "title": "trend title",
      "platform": "platform name",
      "engagement_score": 0,
      "url": "url if available",
      "metadata": {{"analysis": "why this trend works"}}
    }}
  ],
  "content_strategy": [
    {{
      "title": "Content Title",
      "format": "Reel/Short/Post/Story",
      "platform": "recommended platform",
      "best_time": "optimal posting time",
      "hook": "engagement hook strategy",
      "description": "detailed content description"
    }}
  ],
  "analysis_summary": "key insights and patterns identified"
}}
"""

STRATEGY_PROMPT = """
Create a 30-day content calendar based on these analyzed trends:

TRENDS: {top_trends}
TARGET AUDIENCE: {target_audience}
NICHE: {niche}

Generate a JSON array with 30 content items, each containing:
- date, title, format, platform, best_time, hook, description, hashtags, cta

Focus on variety and engagement optimization.
"""
