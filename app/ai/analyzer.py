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

            # Prepare prompt for Groq
            prompt = f"""
            Analyze these trending topics and create a content strategy:

            GOOGLE TRENDS:
            {', '.join([t.get('title', t) if isinstance(t, dict) else str(t) for t in trends_data.google_trends[:5]])}

            REDDIT HOT TOPICS:
            {', '.join([t.get('title', 'Unknown')[:100] for t in trends_data.reddit_trends[:5]])}

            TARGET AUDIENCE: {target_audience}
            NICHE: {niche}

            Create a JSON response with exactly this structure:
            {{
              "top_trends": [
                {{
                  "title": "trend name",
                  "platform": "google_trends or reddit",
                  "engagement_score": 100,
                  "url": "https://example.com",
                  "metadata": {{"analysis": "why this trend works"}}
                }}
              ],
              "content_strategy": [
                {{
                  "title": "Engaging Content Title",
                  "format": "Reel/Short/Post/Story/Carousel",
                  "platform": "Instagram/TikTok",
                  "best_time": "7 PM IST",
                  "hook": "Educational/Challenge/Tips/Tutorial",
                  "description": "Detailed content description"
                }}
              ],
              "analysis_summary": "Key insights and recommendations based on the trends"
            }}

            Return ONLY the JSON object, with no additional text or explanations. Do not wrap the JSON in markdown backticks. Ensure the JSON is well-formed.
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
