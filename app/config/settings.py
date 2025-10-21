"""
Environment Configuration Settings
Centralizes all environment-based configuration using Pydantic Settings
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Settings
    APP_NAME: str = "MusicMood"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database Settings
    DATABASE_URL: str = "postgresql://musicmood_user:musicmood_pass@localhost:5432/musicmood"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10
    REDIS_DECODE_RESPONSES: bool = True
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    OLLAMA_TEMPERATURE: float = 0.7
    OLLAMA_MAX_TOKENS: int = 2000
    OLLAMA_TIMEOUT: int = 30
    
    # Spotify API Settings
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""
    SPOTIFY_REDIRECT_URI: str = "http://localhost:8000/callback"
    
    # OpenWeatherMap API Settings
    OPENWEATHER_API_KEY: str = ""
    
    # API Settings
    API_V1_PREFIX: str = "/api"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8501", "http://localhost:8000"]
    
    # Cache TTL Settings (in seconds)
    MOOD_CACHE_TTL: int = 1800  # 30 minutes
    SEARCH_CACHE_TTL: int = 3600  # 1 hour
    FEATURES_CACHE_TTL: int = 604800  # 7 days
    
    # Agent Settings
    AGENT_MAX_ITERATIONS: int = 5
    AGENT_TIMEOUT: int = 60
    AGENT_VERBOSE: bool = True
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Create global settings instance
settings = Settings()


def validate_settings() -> bool:
    """
    Validate critical settings are present
    Returns True if valid, raises ValueError if invalid
    """
    errors = []
    
    # Check database URL
    if not settings.DATABASE_URL or settings.DATABASE_URL == "":
        errors.append("DATABASE_URL is required")
    
    # Check Ollama URL
    if not settings.OLLAMA_BASE_URL:
        errors.append("OLLAMA_BASE_URL is required")
    
    # Warn about missing API keys (not critical for initial setup)
    if not settings.SPOTIFY_CLIENT_ID:
        print("WARNING: SPOTIFY_CLIENT_ID is not set. Spotify features will not work.")
    
    if not settings.OPENWEATHER_API_KEY:
        print("WARNING: OPENWEATHER_API_KEY is not set. Weather context features will be limited.")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True
