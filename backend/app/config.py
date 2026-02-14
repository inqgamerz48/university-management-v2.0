"""
UniManager Pro - FastAPI Backend Configuration
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Project
    PROJECT_NAME: str = "UniManager Pro API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for UniManager Pro university management system"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/unimanager"
    
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:9002"]
    
    # Storage
    STORAGE_BUCKET: str = "unimanager-files"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Security
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins if it's a string
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            import json
            self.BACKEND_CORS_ORIGINS = json.loads(self.BACKEND_CORS_ORIGINS)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
