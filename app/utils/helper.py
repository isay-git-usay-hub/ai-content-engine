from datetime import datetime
import re
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

def format_timestamp(timestamp: datetime = None) -> str:
    """Format timestamp to ISO string"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\-\.\!\?]', '', text)
    
    return text

def calculate_engagement_score(item: Dict[str, Any]) -> float:
    """Calculate normalized engagement score"""
    platform = item.get('platform', '')
    metadata = item.get('metadata', {})
    
    if platform == 'reddit':
        score = item.get('engagement_score', 0)
        comments = metadata.get('comments', 0)
        return (score * 0.7) + (comments * 0.3)
    
    else:
        return item.get('engagement_score', 0)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def extract_keywords(text: str) -> List[str]:
    """Extract potential keywords from text"""
    words = clean_text(text.lower()).split()
    # Filter out common words and short words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    return keywords[:10]  # Return top 10 keywords
