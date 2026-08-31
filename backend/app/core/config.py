import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

    PROJECT_NAME: str = "FinSight"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-key-change-in-production-finsight-platform"
    REFRESH_SECRET_KEY: str = "super-refresh-secret-key-change-in-production-finsight"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./finsight.db"
    SYNC_DATABASE_URL: str = "sqlite:///./finsight.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 300
    
    RATE_LIMIT_PER_MINUTE: int = 120
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    ML_MODEL_DIR: str = "./ml-engine/models"
    ENABLE_AUTO_RETRAIN: bool = True
    CATEGORIZER_CONFIDENCE_THRESHOLD: float = 0.75
    
    STORAGE_LOCAL_DIR: str = "./storage/reports"
    MAX_UPLOAD_SIZE_BYTES: int = 10485760  # 10 MB
    
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "alerts@finsight.local"
    EMAILS_FROM_NAME: str = "FinSight Financial Alerts"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]

settings = Settings()
