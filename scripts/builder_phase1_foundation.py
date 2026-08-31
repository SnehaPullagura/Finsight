import os
import sys
from scripts.common import write_file

def build_phase1():
    # 1. Project Configuration
    write_file(".gitignore", """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
venv/
ENV/

# Database & SQLite
*.sqlite
*.sqlite3
*.db
!seed*.db

# Testing & Coverage
.pytest_cache/
.coverage
htmlcov/
coverage.xml

# Node & Frontend
frontend/node_modules/
frontend/dist/
frontend/build/
.npm
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE & OS
.idea/
.vscode/
*.swp
*.swo
.DS_Store
Thumbs.db

# ML artifacts / caches
ml-engine/checkpoints/
ml-engine/cache/
*.joblib
!ml-engine/models/*.joblib
!ml-engine/models/*.json
""")

    write_file(".env.example", """
# ==========================================
# FinSight Environment Configuration Example
# ==========================================

PROJECT_NAME="FinSight"
ENVIRONMENT="development"
DEBUG=true
API_V1_STR="/api/v1"
SECRET_KEY="super-secret-key-change-in-production-finsight-platform"
REFRESH_SECRET_KEY="super-refresh-secret-key-change-in-production-finsight"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=14

DATABASE_URL="sqlite+aiosqlite:///./finsight.db"
SYNC_DATABASE_URL="sqlite:///./finsight.db"

REDIS_URL="redis://localhost:6379/0"
CACHE_TTL_SECONDS=300

RATE_LIMIT_PER_MINUTE=120
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=15

ML_MODEL_DIR="./ml-engine/models"
ENABLE_AUTO_RETRAIN=true
CATEGORIZER_CONFIDENCE_THRESHOLD=0.75

STORAGE_LOCAL_DIR="./storage/reports"
MAX_UPLOAD_SIZE_BYTES=10485760

SMTP_HOST="localhost"
SMTP_PORT=1025
SMTP_USER=""
SMTP_PASSWORD=""
EMAILS_FROM_EMAIL="alerts@finsight.local"
EMAILS_FROM_NAME="FinSight Financial Alerts"
""")

    write_file("LICENSE", """
Copyright (c) 2025 FinSight Platform. All rights reserved.

Proprietary and Confidential.
Unauthorized copying of this file or project, via any medium, is strictly prohibited.
Proprietary software for FinSight AI-Powered Financial Health, Cash-Flow Intelligence and Scenario Simulation Platform.
""")

    write_file("pyproject.toml", """
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "finsight-platform"
version = "1.0.0"
description = "AI-Powered Financial Health, Cash-Flow Intelligence and Scenario Simulation Platform"
readme = "README.md"
requires-python = ">=3.11"
authors = [
    { name = "FinSight Engineering Team", email = "engineering@finsight.local" }
]
classifiers = [
    "Private :: Do Not Upload",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Framework :: FastAPI"
]

dependencies = [
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.7.0",
    "pydantic-settings>=2.2.0",
    "sqlalchemy>=2.0.30",
    "alembic>=1.13.0",
    "aiosqlite>=0.20.0",
    "passlib[bcrypt]>=1.7.4",
    "bcrypt>=4.1.0",
    "python-jose[cryptography]>=3.3.0",
    "python-multipart>=0.0.9",
    "redis>=5.0.0",
    "celery>=5.4.0",
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "scikit-learn>=1.4.0",
    "scipy>=1.13.0",
    "reportlab>=4.2.0",
    "openpyxl>=3.1.2",
    "httpx>=0.27.0",
    "rapidfuzz>=3.8.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.2.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0"
]

[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --import-mode=importlib"
testpaths = ["tests"]
python_files = ["test_*.py"]
asyncio_mode = "auto"
""")

    # 2. Backend Core Configuration & Utilities
    write_file("backend/app/__init__.py", '"""FinSight Backend Application Package"""\n__version__ = "1.0.0"\n')
    write_file("backend/app/core/__init__.py", "")

    write_file("backend/app/core/config.py", """
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
""")

    write_file("backend/app/core/security.py", """
import datetime
from typing import Any, Optional, Union, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any],
    claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[datetime.timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "type": "access"
    }
    if claims:
        to_encode.update(claims)
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(
    subject: Union[str, Any],
    claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[datetime.timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "type": "refresh"
    }
    if claims:
        to_encode.update(claims)
    
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None

def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None
""")

    write_file("backend/app/core/masking.py", """
import re
from typing import Any, Dict, List, Union

def mask_account_number(acc_num: str) -> str:
    if not acc_num or len(acc_num) < 4:
        return "XXXX"
    return f"XXXX-XXXX-{acc_num[-4:]}"

def mask_card_number(card_num: str) -> str:
    clean = re.sub(r"\\D", "", card_num or "")
    if len(clean) < 4:
        return "•••• •••• •••• ••••"
    return f"•••• •••• •••• {clean[-4:]}"

def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return "u***@domain.com"
    parts = email.split("@", 1)
    username, domain = parts[0], parts[1]
    if len(username) <= 2:
        masked_user = username[0] + "***"
    else:
        masked_user = username[:2] + "***" + username[-1]
    return f"{masked_user}@{domain}"

def mask_pan_or_tax_id(tax_id: str) -> str:
    if not tax_id or len(tax_id) < 4:
        return "XXXXXX"
    return f"{tax_id[:2]}XXXXX{tax_id[-2:]}"

def sanitize_audit_payload(data: Union[Dict[str, Any], List[Any], Any]) -> Any:
    sensitive_keys = {
        "password", "password_hash", "secret", "token", "refresh_token",
        "access_token", "cvv", "card_number", "pin", "api_key"
    }
    if isinstance(data, dict):
        sanitized = {}
        for k, v in data.items():
            if k.lower() in sensitive_keys:
                sanitized[k] = "[REDACTED]"
            elif isinstance(v, (dict, list)):
                sanitized[k] = sanitize_audit_payload(v)
            else:
                sanitized[k] = v
        return sanitized
    elif isinstance(data, list):
        return [sanitize_audit_payload(item) for item in data]
    return data
""")

    write_file("backend/app/core/logging.py", """
import logging
import sys
import json
from datetime import datetime, timezone

class StructuredJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        if hasattr(record, "request_id"):
            log_obj["request_id"] = getattr(record, "request_id")
        if hasattr(record, "user_id"):
            log_obj["user_id"] = getattr(record, "user_id")
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logger(name: str = "finsight") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()
""")

    write_file("backend/app/core/exceptions.py", """
from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class FinSightException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "An error occurred",
        error_code: str = "GENERIC_ERROR",
        headers: Optional[Dict[str, str]] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
        self.extra = extra or {}

class AuthenticationFailedException(FinSightException):
    def __init__(self, detail: str = "Invalid email or password"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_INVALID_CREDENTIALS",
            headers={"WWW-Authenticate": "Bearer"}
        )

class TokenExpiredException(FinSightException):
    def __init__(self, detail: str = "Authentication token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionDeniedException(FinSightException):
    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTH_PERMISSION_DENIED"
        )

class AccountLockedException(FinSightException):
    def __init__(self, detail: str = "Account temporarily locked due to excessive failed attempts"):
        super().__init__(
            status_code=status.HTTP_423_LOCKED,
            detail=detail,
            error_code="AUTH_ACCOUNT_LOCKED"
        )

class ResourceNotFoundException(FinSightException):
    def __init__(self, resource_name: str = "Resource", resource_id: Any = None):
        detail = f"{resource_name} not found"
        if resource_id:
            detail = f"{resource_name} with ID '{resource_id}' was not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="RESOURCE_NOT_FOUND"
        )

class ValidationConflictException(FinSightException):
    def __init__(self, detail: str = "Resource already exists or violates constraint"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="RESOURCE_CONFLICT"
        )

class RateLimitExceededException(FinSightException):
    def __init__(self, detail: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED"
        )
""")

    write_file("backend/app/core/rate_limit.py", """
import time
from typing import Dict
from collections import defaultdict
from backend.app.core.exceptions import RateLimitExceededException
from backend.app.core.config import settings

class InMemoryRateLimiter:
    def __init__(self):
        self._requests: Dict[str, list] = defaultdict(list)
    
    def check_rate_limit(self, client_key: str, limit: int = 120, window_seconds: int = 60):
        now = time.time()
        window_start = now - window_seconds
        self._requests[client_key] = [
            ts for ts in self._requests[client_key] if ts > window_start
        ]
        if len(self._requests[client_key]) >= limit:
            raise RateLimitExceededException(
                f"Rate limit of {limit} requests per {window_seconds}s exceeded."
            )
        self._requests[client_key].append(now)

rate_limiter = InMemoryRateLimiter()
""")

    # 3. Database Engine & Base
    write_file("backend/app/database/__init__.py", "")

    write_file("backend/app/database/base.py", """
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Integer

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
""")

    write_file("backend/app/database/session.py", """
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def get_sync_db() -> Session:
    db = SyncSessionLocal()
    try:
        return db
    finally:
        pass
""")

    # 4. Identity & Security Models, Schemas, Services, Routers
    write_file("backend/app/auth/__init__.py", "")

    write_file("backend/app/auth/models.py", """
import enum
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class UserRole(str, enum.Enum):
    USER = "user"
    PREMIUM = "premium"
    AUDITOR = "auditor"
    ADMIN = "admin"

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    preferred_currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    security_events: Mapped[List["SecurityEvent"]] = relationship("SecurityEvent", back_populates="user", cascade="all, delete-orphan")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    accounts: Mapped[List["FinancialAccount"]] = relationship("FinancialAccount", back_populates="user", cascade="all, delete-orphan")
    budgets: Mapped[List["Budget"]] = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    goals: Mapped[List["FinancialGoal"]] = relationship("FinancialGoal", back_populates="user", cascade="all, delete-orphan")
    recurring_payments: Mapped[List["RecurringPayment"]] = relationship("RecurringPayment", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    health_scores: Mapped[List["FinancialScore"]] = relationship("FinancialScore", back_populates="user", cascade="all, delete-orphan")
    scenarios: Mapped[List["Scenario"]] = relationship("Scenario", back_populates="user", cascade="all, delete-orphan")

class UserSession(Base, TimestampMixin):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token_jti: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    device_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="sessions")

class SecurityEvent(Base, TimestampMixin):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="security_events")

class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    changes_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
""")

    write_file("backend/app/auth/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from backend.app.auth.models import UserRole

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)
    preferred_currency: str = Field(default="INR", max_length=10)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    device_info: Optional[str] = None

class UserPublicResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    preferred_currency: str
    created_at: datetime.datetime
    last_login_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublicResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class SessionResponse(BaseModel):
    id: int
    device_info: Optional[str]
    ip_address: Optional[str]
    created_at: datetime.datetime
    expires_at: datetime.datetime
    is_revoked: bool

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: Optional[str]
    changes_json: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/auth/service.py", """
import uuid
import json
import datetime
from datetime import timezone
from typing import Optional, Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.app.auth.models import User, UserSession, SecurityEvent, AuditLog, UserRole
from backend.app.auth.schemas import UserRegister, UserLogin
from backend.app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_refresh_token
from backend.app.core.exceptions import (
    AuthenticationFailedException, AccountLockedException, ValidationConflictException,
    ResourceNotFoundException, PermissionDeniedException
)
from backend.app.core.config import settings

class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, data: UserRegister, ip_address: Optional[str] = None) -> User:
        stmt = select(User).where(User.email == data.email.lower())
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise ValidationConflictException("An account with this email address already exists.")
        
        user = User(
            email=data.email.lower(),
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            preferred_currency=data.preferred_currency,
            role=UserRole.USER,
            is_active=True,
            is_verified=True
        )
        db.add(user)
        await db.flush()
        
        event = SecurityEvent(
            user_id=user.id,
            event_type="REGISTER_SUCCESS",
            ip_address=ip_address,
            details=f"User registered with email {user.email}"
        )
        db.add(event)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        login_data: UserLogin,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[User, str, str]:
        stmt = select(User).where(User.email == login_data.email.lower())
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        now = datetime.datetime.now(timezone.utc)
        
        if not user:
            get_password_hash("dummy_password_for_timing")
            raise AuthenticationFailedException()
        
        if user.locked_until and user.locked_until > now:
            minutes_left = int((user.locked_until - now).total_seconds() / 60) + 1
            raise AccountLockedException(f"Account is locked. Please try again in {minutes_left} minutes.")
        
        if not verify_password(login_data.password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user.locked_until = now + datetime.timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
                event = SecurityEvent(
                    user_id=user.id,
                    event_type="ACCOUNT_LOCKED",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details=f"Locked out after {user.failed_login_attempts} failed login attempts"
                )
                db.add(event)
            else:
                event = SecurityEvent(
                    user_id=user.id,
                    event_type="LOGIN_FAILED",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details=f"Failed login attempt ({user.failed_login_attempts}/{settings.MAX_LOGIN_ATTEMPTS})"
                )
                db.add(event)
            await db.commit()
            raise AuthenticationFailedException()
        
        if not user.is_active:
            raise PermissionDeniedException("This account is inactive or disabled.")
        
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = now
        user.last_login_ip = ip_address
        
        jti = str(uuid.uuid4())
        access_token = create_access_token(
            subject=user.id,
            claims={"email": user.email, "role": user.role.value}
        )
        refresh_token = create_refresh_token(
            subject=user.id,
            claims={"jti": jti, "role": user.role.value}
        )
        
        session = UserSession(
            user_id=user.id,
            refresh_token_jti=jti,
            device_info=login_data.device_info or "Unknown Device",
            ip_address=ip_address,
            user_agent=user_agent,
            is_revoked=False,
            expires_at=now + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(session)
        
        event = SecurityEvent(
            user_id=user.id,
            event_type="LOGIN_SUCCESS",
            ip_address=ip_address,
            user_agent=user_agent,
            details=f"Successful login from {ip_address}"
        )
        db.add(event)
        
        await db.commit()
        await db.refresh(user)
        return user, access_token, refresh_token

    @staticmethod
    async def refresh_tokens(
        db: AsyncSession,
        refresh_token_str: str,
        ip_address: Optional[str] = None
    ) -> Tuple[User, str, str]:
        payload = decode_refresh_token(refresh_token_str)
        if not payload:
            raise AuthenticationFailedException("Invalid or expired refresh token")
        
        user_id = int(payload.get("sub"))
        jti = payload.get("jti")
        
        stmt = select(UserSession).where(UserSession.refresh_token_jti == jti)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session or session.is_revoked:
            raise AuthenticationFailedException("Session revoked or expired")
        
        user_stmt = select(User).where(User.id == user_id)
        user_res = await db.execute(user_stmt)
        user = user_res.scalar_one_or_none()
        if not user or not user.is_active:
            raise AuthenticationFailedException("User not found or inactive")
        
        session.is_revoked = True
        
        new_jti = str(uuid.uuid4())
        new_access_token = create_access_token(
            subject=user.id,
            claims={"email": user.email, "role": user.role.value}
        )
        new_refresh_token = create_refresh_token(
            subject=user.id,
            claims={"jti": new_jti, "role": user.role.value}
        )
        
        now = datetime.datetime.now(timezone.utc)
        new_session = UserSession(
            user_id=user.id,
            refresh_token_jti=new_jti,
            device_info=session.device_info,
            ip_address=ip_address or session.ip_address,
            user_agent=session.user_agent,
            is_revoked=False,
            expires_at=now + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_session)
        await db.commit()
        
        return user, new_access_token, new_refresh_token

    @staticmethod
    async def logout_session(db: AsyncSession, user_id: int) -> bool:
        await db.execute(
            update(UserSession)
            .where(UserSession.user_id == user_id)
            .values(is_revoked=True)
        )
        await db.commit()
        return True
""")

    write_file("backend/app/auth/dependencies.py", """
from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.database.session import get_db
from backend.app.auth.models import User, UserRole
from backend.app.core.security import decode_access_token
from backend.app.core.exceptions import AuthenticationFailedException, TokenExpiredException, PermissionDeniedException

security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if not credentials or not credentials.credentials:
        raise AuthenticationFailedException("Missing or invalid Authorization header")
    
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise TokenExpiredException()
    
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationFailedException("Token missing subject identifier")
    
    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise AuthenticationFailedException("User not found")
    if not user.is_active:
        raise PermissionDeniedException("User account is inactive")
    
    return user

async def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise PermissionDeniedException("Administrative privileges required")
    return current_user
""")

    write_file("backend/app/auth/router.py", """
from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.schemas import (
    UserRegister, UserLogin, TokenResponse, RefreshTokenRequest,
    UserPublicResponse, SessionResponse
)
from backend.app.auth.service import AuthService
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User, UserSession
from backend.app.core.config import settings
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["Identity & Security"])

@router.post("/register", response_model=UserPublicResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_address = request.client.host if request.client else "127.0.0.1"
    user = await AuthService.register_user(db, data, ip_address=ip_address)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_address = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("user-agent", "Unknown")
    user, access_token, refresh_token = await AuthService.authenticate_user(
        db, data, ip_address=ip_address, user_agent=user_agent
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserPublicResponse.model_validate(user)
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    ip_address = request.client.host if request.client else "127.0.0.1"
    user, access_token, refresh_token = await AuthService.refresh_tokens(
        db, data.refresh_token, ip_address=ip_address
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserPublicResponse.model_validate(user)
    )

@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AuthService.logout_session(db, current_user.id)
    return {"message": "Successfully logged out from all active sessions."}

@router.get("/me", response_model=UserPublicResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/sessions", response_model=List[SessionResponse])
async def list_user_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(UserSession).where(
        UserSession.user_id == current_user.id
    ).order_by(UserSession.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()
""")

    # 5. Financial Accounts Models, Schemas, Services, Routers
    write_file("backend/app/accounts/__init__.py", "")

    write_file("backend/app/accounts/models.py", """
import enum
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class AccountType(str, enum.Enum):
    BANK = "bank"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    CASH = "cash"
    LOAN = "loan"
    INVESTMENT = "investment"

class AccountStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class FinancialAccount(Base, TimestampMixin):
    __tablename__ = "financial_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(SQLEnum(AccountType), nullable=False)
    account_number_masked: Mapped[str] = mapped_column(String(64), default="XXXX", nullable=False)
    institution_name: Mapped[str] = mapped_column(String(128), default="Self/Manual", nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    
    current_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    available_balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    credit_limit: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    interest_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    status: Mapped[AccountStatus] = mapped_column(SQLEnum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_reconciled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="accounts")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    balance_history: Mapped[List["AccountBalanceHistory"]] = relationship("AccountBalanceHistory", back_populates="account", cascade="all, delete-orphan")

class AccountBalanceHistory(Base, TimestampMixin):
    __tablename__ = "account_balance_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("financial_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    snapshot_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    change_reason: Mapped[str] = mapped_column(String(128), default="transaction_sync")

    account: Mapped["FinancialAccount"] = relationship("FinancialAccount", back_populates="balance_history")
""")

    write_file("backend/app/accounts/schemas.py", """
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from backend.app.accounts.models import AccountType, AccountStatus

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    account_type: AccountType
    account_number: Optional[str] = Field(default=None, max_length=64)
    institution_name: Optional[str] = Field(default="Self/Manual", max_length=128)
    currency: str = Field(default="INR", max_length=10)
    current_balance: float = Field(default=0.0)
    credit_limit: Optional[float] = None
    interest_rate: Optional[float] = None
    is_primary: bool = False
    notes: Optional[str] = None

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    institution_name: Optional[str] = None
    current_balance: Optional[float] = None
    credit_limit: Optional[float] = None
    interest_rate: Optional[float] = None
    status: Optional[AccountStatus] = None
    is_primary: bool = False
    notes: Optional[str] = None

class AccountResponse(BaseModel):
    id: int
    user_id: int
    name: str
    account_type: AccountType
    account_number_masked: str
    institution_name: str
    currency: str
    current_balance: float
    available_balance: float
    credit_limit: Optional[float] = None
    interest_rate: Optional[float] = None
    status: AccountStatus
    is_primary: bool
    last_reconciled_at: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class BalanceHistoryResponse(BaseModel):
    id: int
    account_id: int
    balance: float
    snapshot_date: datetime.datetime
    change_reason: str

    class Config:
        from_attributes = True

class AccountReconcileRequest(BaseModel):
    actual_balance: float
    notes: Optional[str] = None
""")

    write_file("backend/app/accounts/service.py", """
import datetime
from datetime import timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.app.accounts.models import FinancialAccount, AccountBalanceHistory, AccountStatus
from backend.app.accounts.schemas import AccountCreate, AccountUpdate, AccountReconcileRequest
from backend.app.core.masking import mask_account_number
from backend.app.core.exceptions import ResourceNotFoundException

class AccountService:
    @staticmethod
    async def create_account(db: AsyncSession, user_id: int, data: AccountCreate) -> FinancialAccount:
        masked_num = mask_account_number(data.account_number or "0000")
        
        if data.is_primary:
            await db.execute(
                update(FinancialAccount)
                .where(FinancialAccount.user_id == user_id)
                .values(is_primary=False)
            )
        
        account = FinancialAccount(
            user_id=user_id,
            name=data.name,
            account_type=data.account_type,
            account_number_masked=masked_num,
            institution_name=data.institution_name or "Manual",
            currency=data.currency,
            current_balance=data.current_balance,
            available_balance=data.current_balance,
            credit_limit=data.credit_limit,
            interest_rate=data.interest_rate,
            is_primary=data.is_primary,
            status=AccountStatus.ACTIVE,
            notes=data.notes
        )
        db.add(account)
        await db.flush()
        
        history = AccountBalanceHistory(
            account_id=account.id,
            balance=data.current_balance,
            snapshot_date=datetime.datetime.now(timezone.utc),
            change_reason="initial_creation"
        )
        db.add(history)
        await db.commit()
        await db.refresh(account)
        return account

    @staticmethod
    async def list_accounts(db: AsyncSession, user_id: int) -> List[FinancialAccount]:
        stmt = select(FinancialAccount).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status != AccountStatus.ARCHIVED
        ).order_by(FinancialAccount.is_primary.desc(), FinancialAccount.name.asc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_account(db: AsyncSession, user_id: int, account_id: int) -> FinancialAccount:
        stmt = select(FinancialAccount).where(
            FinancialAccount.id == account_id,
            FinancialAccount.user_id == user_id
        )
        result = await db.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            raise ResourceNotFoundException("Financial Account", account_id)
        return account

    @staticmethod
    async def update_account(db: AsyncSession, user_id: int, account_id: int, data: AccountUpdate) -> FinancialAccount:
        account = await AccountService.get_account(db, user_id, account_id)
        update_dict = data.model_dump(exclude_unset=True)
        if update_dict.get("is_primary"):
            await db.execute(
                update(FinancialAccount)
                .where(FinancialAccount.user_id == user_id)
                .values(is_primary=False)
            )
        for k, v in update_dict.items():
            setattr(account, k, v)
        if "current_balance" in update_dict and update_dict["current_balance"] is not None:
            account.available_balance = update_dict["current_balance"]
            history = AccountBalanceHistory(
                account_id=account.id,
                balance=account.current_balance,
                snapshot_date=datetime.datetime.now(timezone.utc),
                change_reason="manual_update"
            )
            db.add(history)
        await db.commit()
        await db.refresh(account)
        return account

    @staticmethod
    async def reconcile_account(
        db: AsyncSession, user_id: int, account_id: int, data: AccountReconcileRequest
    ) -> FinancialAccount:
        account = await AccountService.get_account(db, user_id, account_id)
        diff = data.actual_balance - account.current_balance
        account.current_balance = data.actual_balance
        account.available_balance = data.actual_balance
        account.last_reconciled_at = datetime.datetime.now(timezone.utc)
        
        history = AccountBalanceHistory(
            account_id=account.id,
            balance=account.current_balance,
            snapshot_date=account.last_reconciled_at,
            change_reason=f"reconciliation (adjustment: {diff:+.2f})"
        )
        db.add(history)
        await db.commit()
        await db.refresh(account)
        return account

    @staticmethod
    async def delete_account(db: AsyncSession, user_id: int, account_id: int) -> bool:
        account = await AccountService.get_account(db, user_id, account_id)
        account.status = AccountStatus.ARCHIVED
        await db.commit()
        return True
""")

    write_file("backend/app/accounts/router.py", """
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.accounts.schemas import (
    AccountCreate, AccountUpdate, AccountResponse, BalanceHistoryResponse, AccountReconcileRequest
)
from backend.app.accounts.service import AccountService
from backend.app.accounts.models import AccountBalanceHistory
from sqlalchemy import select

router = APIRouter(prefix="/accounts", tags=["Financial Accounts"])

@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.create_account(db, current_user.id, data)

@router.get("", response_model=List[AccountResponse])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.list_accounts(db, current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.get_account(db, current_user.id, account_id)

@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    data: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.update_account(db, current_user.id, account_id, data)

@router.post("/{account_id}/reconcile", response_model=AccountResponse)
async def reconcile_account(
    account_id: int,
    data: AccountReconcileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.reconcile_account(db, current_user.id, account_id, data)

@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AccountService.delete_account(db, current_user.id, account_id)
    return {"message": "Account archived successfully"}

@router.get("/{account_id}/history", response_model=List[BalanceHistoryResponse])
async def get_balance_history(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AccountService.get_account(db, current_user.id, account_id)
    stmt = select(AccountBalanceHistory).where(
        AccountBalanceHistory.account_id == account_id
    ).order_by(AccountBalanceHistory.snapshot_date.desc()).limit(100)
    res = await db.execute(stmt)
    return list(res.scalars().all())
""")

    # 6. Categories & Taxonomy
    write_file("backend/app/categories/__init__.py", "")

    write_file("backend/app/categories/models.py", """
import enum
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class CategoryGroup(str, enum.Enum):
    INCOME = "income"
    ESSENTIAL_EXPENSE = "essential_expense"
    DISCRETIONARY_EXPENSE = "discretionary_expense"
    SAVINGS_INVESTMENT = "savings_investment"
    DEBT_EMI = "debt_emi"
    TRANSFER = "transfer"

class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    group: Mapped[CategoryGroup] = mapped_column(SQLEnum(CategoryGroup), nullable=False, index=True)
    icon: Mapped[str] = mapped_column(String(64), default="Tag", nullable=False)
    color: Mapped[str] = mapped_column(String(16), default="#6366F1", nullable=False)
    is_tax_deductible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_system_default: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="category")
    budgets: Mapped[List["Budget"]] = relationship("Budget", back_populates="category")
""")

    write_file("backend/app/categories/schemas.py", """
from typing import Optional, List
from pydantic import BaseModel, Field
from backend.app.categories.models import CategoryGroup

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=64)
    group: CategoryGroup
    icon: Optional[str] = "Tag"
    color: Optional[str] = "#6366F1"
    is_tax_deductible: bool = False

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    group: CategoryGroup
    icon: str
    color: str
    is_tax_deductible: bool
    is_system_default: bool

    class Config:
        from_attributes = True
""")

    write_file("backend/app/categories/service.py", """
import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.categories.models import Category, CategoryGroup

DEFAULT_CATEGORIES = [
    {"name": "Salary & Wages", "group": CategoryGroup.INCOME, "icon": "Briefcase", "color": "#10B981"},
    {"name": "Business & Freelance", "group": CategoryGroup.INCOME, "icon": "Laptop", "color": "#059669"},
    {"name": "Dividends & Interest", "group": CategoryGroup.INCOME, "icon": "TrendingUp", "color": "#34D399"},
    {"name": "Rental Income", "group": CategoryGroup.INCOME, "icon": "Home", "color": "#6EE7B7"},
    {"name": "Refunds & Reimbursements", "group": CategoryGroup.INCOME, "icon": "RotateCcw", "color": "#A7F3D0"},
    {"name": "Other Income", "group": CategoryGroup.INCOME, "icon": "PlusCircle", "color": "#047857"},
    
    {"name": "Housing & Rent", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Home", "color": "#EF4444"},
    {"name": "Groceries & Supermarket", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "ShoppingCart", "color": "#F97316"},
    {"name": "Utilities & Electricity", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Zap", "color": "#F59E0B"},
    {"name": "Healthcare & Pharmacy", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "HeartPulse", "color": "#EC4899"},
    {"name": "Fuel & Commute", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Fuel", "color": "#84CC16"},
    {"name": "Insurance Premiums", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "ShieldCheck", "color": "#06B6D4", "is_tax_deductible": True},
    {"name": "Education & Tuition", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "GraduationCap", "color": "#3B82F6", "is_tax_deductible": True},
    {"name": "Mobile & Internet", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Wifi", "color": "#6366F1"},
    
    {"name": "Dining Out & Cafes", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Utensils", "color": "#FB923C"},
    {"name": "Food Delivery", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Bike", "color": "#F87171"},
    {"name": "Entertainment & Movies", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Film", "color": "#A855F7"},
    {"name": "Shopping & Apparel", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "ShoppingBag", "color": "#EC4899"},
    {"name": "Travel & Vacation", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Plane", "color": "#0EA5E9"},
    {"name": "Subscriptions & Streaming", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Tv", "color": "#8B5CF6"},
    {"name": "Personal Care & Grooming", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Sparkles", "color": "#D946EF"},
    {"name": "Gifts & Donations", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Gift", "color": "#14B8A6"},
    
    {"name": "Mutual Funds & SIP", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "BarChart3", "color": "#3B82F6"},
    {"name": "Fixed Deposits & RD", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "PiggyBank", "color": "#2563EB"},
    {"name": "Stocks & Equity", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "LineChart", "color": "#1D4ED8"},
    {"name": "Gold & Commodities", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "Coins", "color": "#D97706"},
    {"name": "Retirement & PPF", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "Shield", "color": "#4F46E5", "is_tax_deductible": True},
    
    {"name": "Home Loan EMI", "group": CategoryGroup.DEBT_EMI, "icon": "Building", "color": "#DC2626", "is_tax_deductible": True},
    {"name": "Car Loan EMI", "group": CategoryGroup.DEBT_EMI, "icon": "Car", "color": "#B91C1C"},
    {"name": "Personal Loan EMI", "group": CategoryGroup.DEBT_EMI, "icon": "CreditCard", "color": "#991B1B"},
    {"name": "Credit Card Bill", "group": CategoryGroup.DEBT_EMI, "icon": "Receipt", "color": "#7F1D1D"},
    
    {"name": "Account Transfer", "group": CategoryGroup.TRANSFER, "icon": "ArrowLeftRight", "color": "#64748B"},
    {"name": "ATM Cash Withdrawal", "group": CategoryGroup.TRANSFER, "icon": "Banknote", "color": "#475569"}
]

class CategoryService:
    @staticmethod
    async def seed_defaults(db: AsyncSession):
        for cat_data in DEFAULT_CATEGORIES:
            slug = re.sub(r"[^a-z0-9]+", "-", cat_data["name"].lower()).strip("-")
            stmt = select(Category).where(Category.slug == slug)
            res = await db.execute(stmt)
            if not res.scalar_one_or_none():
                cat = Category(
                    name=cat_data["name"],
                    slug=slug,
                    group=cat_data["group"],
                    icon=cat_data.get("icon", "Tag"),
                    color=cat_data.get("color", "#6366F1"),
                    is_tax_deductible=cat_data.get("is_tax_deductible", False),
                    is_system_default=True
                )
                db.add(cat)
        await db.commit()

    @staticmethod
    async def list_categories(db: AsyncSession) -> List[Category]:
        stmt = select(Category).order_by(Category.group.asc(), Category.name.asc())
        result = await db.execute(stmt)
        categories = list(result.scalars().all())
        if not categories:
            await CategoryService.seed_defaults(db)
            result = await db.execute(stmt)
            categories = list(result.scalars().all())
        return categories
""")

    write_file("backend/app/categories/router.py", """
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.categories.schemas import CategoryResponse
from backend.app.categories.service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories & Taxonomy"])

@router.get("", response_model=List[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryService.list_categories(db)
""")

    print("Phase 1 files built successfully!")

if __name__ == "__main__":
    build_phase1()
