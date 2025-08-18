class AIContentEngineError(Exception):
    """Base exception for AI Content Engine"""
    pass

class DataCollectionError(AIContentEngineError):
    """Raised when data collection fails"""
    def __init__(self, platform: str, message: str):
        self.platform = platform
        self.message = message
        super().__init__(f"Data collection failed for {platform}: {message}")

class AIAnalysisError(AIContentEngineError):
    """Raised when AI analysis fails"""
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(f"AI analysis failed: {message}")

class ValidationError(AIContentEngineError):
    """Raised when data validation fails"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error for {field}: {message}")

class RateLimitError(AIContentEngineError):
    """Raised when API rate limit is exceeded"""
    def __init__(self, platform: str, retry_after: int = None):
        self.platform = platform
        self.retry_after = retry_after
        message = f"Rate limit exceeded for {platform}"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message)
