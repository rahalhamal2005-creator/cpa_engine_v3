import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    youtube_api_key: str = os.getenv("YOUTUBE_API_KEY", "")
    serp_api_key: str = os.getenv("SERP_API_KEY", "")
    tiktok_api_key: str = os.getenv("TIKTOK_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Updated to read from Render / Cloud instead of local SQLite by default
    # If DATABASE_URL is not set, it falls back to local sqlite for your PC
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./cpa_engine.db")

    class Config:
        env_file = ".env"

settings = Settings()
