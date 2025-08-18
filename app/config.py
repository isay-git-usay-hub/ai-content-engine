from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Groq AI Settings (instead of Gemini)
    GROQ_API_KEY: str = ""
    AI_MODEL: str = "llama3-8b-8192"  # or "mixtral-8x7b-32768"
    MAX_TOKENS: int = 1500
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Data Collection
    REDDIT_USER_AGENT: str = "AIContentEngine/1.0"
    TRENDS_LIMIT: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()  # ← Fixed: Added missing instantiation
