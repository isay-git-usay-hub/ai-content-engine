import json
import logging
import re
from app.models import TrendingData, StrategyResponse, TrendItem, ContentRecommendation
from app.config import settings
from groq import Groq
from .prompts import ANALYSIS_PROMPT

logger = logging.getLogger(__name__)

# Compile regex for cleaning control characters
# This regex removes characters with ASCII values from 0 to 31, except for tab, newline, and carriage return.
CLEAN_JSON_REGEX = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

class AIAnalyzer:
    def __init__(self):
        try:
            # Check if API key exists
            if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "":
                logger.error("Groq API key not found in environment variables")
                raise ValueError("Groq API key is required")

            # Initialize Groq client
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = settings.AI_MODEL
            self.max_tokens = settings.MAX_TOKENS
            logger.info("Groq client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            raise

    async def analyze_trends(self, trends_data: TrendingData, target_audience: str = "Gen Z", niche: str = "General") -> StrategyResponse:
        try:
            # Log the input data
            logger.info(f"Analyzing trends for {target_audience} in {niche} niche")
            logger.info(f"Google trends count: {len(trends_data.google_trends)}")
            logger.info(f"Reddit trends count: {len(trends_data.reddit_trends)}")

            # Check if we have any data to analyze
            if not trends_data.google_trends and not trends_data.reddit_trends:
                logger.error("No trending data available for analysis")
                raise ValueError("No trending data available for analysis")

            # Prepare a more sophisticated prompt for Groq
            prompt = f"""
As an expert social media strategist and content creator, your task is to analyze the provided trends and devise a highly creative and effective content strategy for the specified audience and niche.

**Analysis Data:**
- **Google Trends:** {', '.join([t.get('title', 'Unknown') for t in trends_data.google_trends[:5]])}
- **Reddit Hot Topics:** {', '.join([t.get('title', 'Unknown')[:100] for t in trends_data.reddit_trends[:5]])}
- **Target Audience:** {target_audience}
- **Niche:** {niche}

**Your Mission:**
Generate a short, 3-day content plan. For each day, provide one unique and compelling content idea. The ideas should be a mix of formats and platforms to maximize reach and engagement.

**Output Requirements:**
You must return ONLY a single, well-formed JSON object. Do not include any text, explanations, or markdown formatting before or after the JSON. The JSON must conform to the following structure exactly:

{{
  "top_trends": [
    {{
      "title": "The most relevant trend title",
      "platform": "google_trends or reddit",
      "engagement_score": 850,
      "url": "https://example.com/trend",
      "metadata": {{
        "analysis": "A brief, insightful analysis of why this trend is relevant and how it can be leveraged for the target audience."
      }}
    }}
  ],
  "content_strategy": [
    {{
      "title": "Example: '3 AI Tools That Will Change How You Work'",
      "format": "Short-Form Video (e.g., Reel, TikTok, Short)",
      "platform": "Instagram",
      "best_time": "8:00 PM",
      "hook": "A killer opening line to grab attention in the first 3 seconds. Example: 'Stop scrolling! This AI tool does your work for you.'",
      "description": "A detailed, engaging description for the post. Include a compelling narrative, relevant hashtags (3-5), and a clear call-to-action (CTA). Example: 'Ever feel overwhelmed? These 3 AI tools are game-changers... 1. Tool A... 2. Tool B... 3. Tool C... Which one will you try first? Let me know! #AI #Productivity #Tech'",
      "visual_idea": "A suggestion for the visuals. Example: 'Fast-paced video showing the UI of each tool in action, with dynamic text overlays and a trending audio track.'"
    }},
    {{
      "title": "Example: 'The Ultimate Guide to [Relevant Trend]'",
      "format": "Carousel Post / Blog Post",
      "platform": "LinkedIn",
      "best_time": "9:00 AM",
      "hook": "An intriguing question or a bold statement. Example: 'Is [Relevant Trend] the future of [Niche]?'",
      "description": "In-depth content providing real value. Use bullet points or numbered lists for readability. End with a question to encourage comments. Example: 'Deep dive into [Relevant Trend]... 1. What it is... 2. Why it matters... 3. How to get started... What are your thoughts on this? #TechTrends #[Niche]'",
      "visual_idea": "A visually appealing carousel with a strong title slide, followed by slides breaking down each point with clean icons and minimal text."
    }}
  ],
  "analysis_summary": "A concise, high-level summary of the key insights from the trends and the strategic recommendations for the content plan."
}}
"""

            logger.info("Sending request to Groq")

            # Make request to Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            logger.info(f"Received response from Groq: {ai_response[:200]}...")

            # Clean response (remove markdown and extract JSON)
            clean_response = ai_response.strip().replace('`json', '').replace('`', '')

            # More robust JSON extraction
            json_start = clean_response.find('{')
            json_end = clean_response.rfind('}') + 1

            if json_start != -1 and json_end > json_start:
                json_str = clean_response[json_start:json_end]
                try:
                    # Sanitize the JSON string by removing invalid control characters
                    sanitized_json_str = CLEAN_JSON_REGEX.sub('', json_str)
                    
                    # Attempt to fix common JSON errors, like trailing commas
                    fixed_json_str = re.sub(r",(\s*[\]}])", r"\1", sanitized_json_str)
                    
                    parsed_response = json.loads(fixed_json_str)
                    return StrategyResponse(**parsed_response)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Groq JSON: {e}")
                    logger.error(f"Raw response from Groq: {ai_response}")
                    logger.error(f"Attempted to clean and parse this JSON string: {fixed_json_str}")
                    raise ValueError(f"Failed to parse Groq response: {str(e)}")
            else:
                logger.error("No valid JSON found in Groq response")
                logger.error(f"Raw response from Groq: {ai_response}")
                raise ValueError("No valid JSON found in Groq response")

        except Exception as e:
            logger.error(f"Error in Groq analysis: {str(e)}")
            raise
