import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "ClientFlow CRM"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str = "super_secure_clientflow_enterprise_secret_key_2026_change_in_prod"
    APP_URL: str = "http://localhost:3000"
    API_V1_PREFIX: str = "/api/v1"

    # Security & CORS
    ALLOWED_ORIGINS: Union[List[str], str] = ["*", "http://localhost:5173", "http://localhost:3000", "http://localhost:80", "http://localhost:8000", "http://127.0.0.1:5173", "http://127.0.0.1:8000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALGORITHM: str = "HS256"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "clientflow_db"
    POSTGRES_USER: str = "clientflow_user"
    POSTGRES_PASSWORD: str = "clientflow_secret_password"
    DATABASE_URL: str = "sqlite+aiosqlite:///./clientflow.db"
    DATABASE_SYNC_URL: str = "sqlite:///./clientflow.db"

    # Redis & Workers
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # OpenSearch
    OPENSEARCH_HOST: str = "localhost"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_USER: str = "admin"
    OPENSEARCH_PASSWORD: str = "admin"
    OPENSEARCH_USE_SSL: bool = False

    # Storage
    STORAGE_PROVIDER: str = "local"
    STORAGE_LOCAL_ROOT: str = "./media_uploads"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "clientflow-documents"

    # Communication Providers
    EMAIL_PROVIDER: str = "mock"
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = False
    EMAILS_FROM_EMAIL: str = "no-reply@clientflow.internal"
    EMAILS_FROM_NAME: str = "ClientFlow CRM"
    SMS_PROVIDER: str = "mock"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_FROM_NUMBER: str = ""

    # AI Assistant
    AI_PROVIDER: str = "mock"
    AI_MODEL_NAME: str = "gemini-1.5-pro"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 120

settings = Settings()
