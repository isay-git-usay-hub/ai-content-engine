from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseCollector(ABC):
    """Base class for all data collectors"""
    
    def __init__(self, limit: int = 10):
        self.limit = limit
        self.platform_name = self.__class__.__name__.replace('Collector', '').lower()
    
    @abstractmethod
    async def collect(self) -> List[Dict[str, Any]]:
        """Collect trending data from the platform"""
        pass
    
    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean collected data"""
        return [item for item in data if item.get('title')]
    
    def format_data(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Format platform-specific data to standard format"""
        return raw_data
