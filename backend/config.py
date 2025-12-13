"""
Application configuration using Pydantic Settings.
Loads from environment variables with .env file support.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""
    
    # Environment
    ENV: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./finance_coach.db"
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI/ML APIs
    OPENROUTER_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # Email (Optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Backend
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    
    # Frontend
    API_BASE_URL: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
