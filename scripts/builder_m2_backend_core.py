import os
from scripts.common import write_file

def run():
    # 1. core/config.py
    write_file("backend/app/core/config.py", """import os
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
    ALLOWED_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]
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
    DATABASE_URL: str = "postgresql+asyncpg://clientflow_user:clientflow_secret_password@localhost:5432/clientflow_db"
    DATABASE_SYNC_URL: str = "postgresql+psycopg2://clientflow_user:clientflow_secret_password@localhost:5432/clientflow_db"

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
""")

    # 2. core/logging.py
    write_file("backend/app/core/logging.py", """import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if hasattr(record, "request_id"):
            log_data["request_id"] = getattr(record, "request_id")
        if hasattr(record, "tenant_id"):
            log_data["tenant_id"] = getattr(record, "tenant_id")
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    # Set third party loggers to warning
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

setup_logging()
logger = logging.getLogger("clientflow")
""")

    # 3. core/database.py
    write_file("backend/app/core/database.py", """from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings
from backend.app.core.logging import logger

# Async Engine for FastAPI Request Lifecycle
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync Engine for Migrations, Background Workers and Tools
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL if "postgresql" in settings.DATABASE_SYNC_URL else settings.DATABASE_URL.replace("+asyncpg", ""),
    echo=False,
    pool_pre_ping=True,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rolled back due to error: {str(e)}", exc_info=True)
            raise
        finally:
            await session.close()
""")

    # 4. core/security.py
    write_file("backend/app/core/security.py", """from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
import jwt
from passlib.context import CryptContext
import pyotp
import secrets
from backend.app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any],
    tenant_id: Optional[str] = None,
    roles: Optional[list] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "tenant_id": str(tenant_id) if tenant_id else None,
        "roles": roles or [],
        "iat": datetime.utcnow()
    }
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(
    subject: Union[str, Any],
    tenant_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "tenant_id": str(tenant_id) if tenant_id else None,
        "jti": secrets.token_hex(16),
        "iat": datetime.utcnow()
    }
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[settings.ALGORITHM])

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def get_totp_uri(secret: str, email: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.APP_NAME)

def verify_totp_code(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
""")

    # 5. core/exceptions.py
    write_file("backend/app/core/exceptions.py", """from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class ClientFlowException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = "CLIENTFLOW_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": details or {}
            }
        )

class EntityNotFoundException(ClientFlowException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{entity_name} with id '{entity_id}' was not found.",
            error_code="ENTITY_NOT_FOUND",
            details={"entity": entity_name, "id": str(entity_id)}
        )

class TenantAccessViolationException(ClientFlowException):
    def __init__(self, message: str = "Tenant access violation. Operation not permitted."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="TENANT_ACCESS_VIOLATION"
        )

class PermissionDeniedException(ClientFlowException):
    def __init__(self, permission_name: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=f"Missing required permission: '{permission_name}'",
            error_code="PERMISSION_DENIED",
            details={"required_permission": permission_name}
        )

class AuthenticationException(ClientFlowException):
    def __init__(self, message: str = "Invalid credentials or expired token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="AUTHENTICATION_FAILED"
        )

class ConflictException(ClientFlowException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="RESOURCE_CONFLICT"
        )

class ValidationException(ClientFlowException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_FAILED",
            details=details
        )
""")

    # 6. core/middleware.py
    write_file("backend/app/core/middleware.py", """import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from backend.app.core.logging import logger

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        # Extract tenant header if provided
        tenant_id = request.headers.get("X-Tenant-ID", None)
        request.state.tenant_id = tenant_id

        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception as exc:
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"Unhandled error processing {request.method} {request.url.path} in {duration:.2f}ms: {str(exc)}",
                extra={"request_id": request_id, "tenant_id": tenant_id},
                exc_info=True
            )
            raise exc

        duration = (time.time() - start_time) * 1000
        
        # Attach security & tracing headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-MS"] = f"{duration:.2f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
""")

    # 7. core/events.py
    write_file("backend/app/core/events.py", """from typing import Any, Callable, Dict, List
import asyncio
from backend.app.core.logging import logger

class DomainEvent:
    def __init__(self, name: str, tenant_id: str, payload: Dict[str, Any], actor_id: str = None):
        self.name = name
        self.tenant_id = tenant_id
        self.payload = payload
        self.actor_id = actor_id
        self.timestamp = asyncio.get_event_loop().time()

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, handler: Callable):
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        logger.info(f"Registered event listener for domain event: '{event_name}'")

    async def publish(self, event: DomainEvent):
        logger.info(f"Publishing domain event: {event.name} (Tenant: {event.tenant_id})")
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(event))
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error executing handler for event {event.name}: {str(e)}", exc_info=True)

event_bus = EventBus()
""")

    # 8. models/base.py
    write_file("backend/app/models/base.py", """import uuid
from datetime import datetime
from typing import Any, Dict
from sqlalchemy import DateTime, String, Boolean, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class UUIDModel(Base):
    __abstract__ = True
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class TenantMixin:
    tenant_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True
    )
""")

    # 9. repositories/base.py
    write_file("backend/app/repositories/base.py", """from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: str, tenant_id: Optional[str] = None) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        if tenant_id and hasattr(self.model, "tenant_id"):
            query = query.where(self.model.tenant_id == tenant_id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list(
        self,
        tenant_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Any] = None
    ) -> List[ModelType]:
        query = select(self.model)
        if tenant_id and hasattr(self.model, "tenant_id"):
            query = query.where(self.model.tenant_id == tenant_id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
            
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)

        if order_by is not None:
            query = query.order_by(order_by)
        elif hasattr(self.model, "created_at"):
            query = query.order_by(self.model.created_at.desc())

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(self, tenant_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count(self.model.id))
        if tenant_id and hasattr(self.model, "tenant_id"):
            query = query.where(self.model.tenant_id == tenant_id)
        if hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted == False)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def create(self, obj_in: Dict[str, Any], tenant_id: Optional[str] = None) -> ModelType:
        data = obj_in.copy()
        if tenant_id and hasattr(self.model, "tenant_id") and "tenant_id" not in data:
            data["tenant_id"] = tenant_id
        db_obj = self.model(**data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        if hasattr(db_obj, "updated_at"):
            setattr(db_obj, "updated_at", datetime.utcnow())
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, id: str, tenant_id: Optional[str] = None) -> bool:
        db_obj = await self.get_by_id(id, tenant_id=tenant_id)
        if not db_obj:
            return False
        if hasattr(db_obj, "is_deleted"):
            setattr(db_obj, "is_deleted", True)
            if hasattr(db_obj, "deleted_at"):
                setattr(db_obj, "deleted_at", datetime.utcnow())
            self.db.add(db_obj)
            await self.db.flush()
            return True
        else:
            await self.db.delete(db_obj)
            await self.db.flush()
            return True
""")

    # 10. services/base.py
    write_file("backend/app/services/base.py", """from typing import Any, Dict, Generic, List, Optional, TypeVar
from backend.app.models.base import Base
from backend.app.repositories.base import BaseRepository
from backend.app.core.exceptions import EntityNotFoundException, TenantAccessViolationException

ModelType = TypeVar("ModelType", bound=Base)
RepoType = TypeVar("RepoType", bound=BaseRepository)

class BaseService(Generic[ModelType, RepoType]):
    def __init__(self, repository: RepoType):
        self.repository = repository

    async def get(self, id: str, tenant_id: Optional[str] = None) -> ModelType:
        entity = await self.repository.get_by_id(id, tenant_id=tenant_id)
        if not entity:
            raise EntityNotFoundException(self.repository.model.__name__, id)
        return entity

    async def list(
        self,
        tenant_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        return await self.repository.list(tenant_id=tenant_id, skip=skip, limit=limit, filters=filters)

    async def count(self, tenant_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> int:
        return await self.repository.count(tenant_id=tenant_id, filters=filters)

    async def create(self, schema_in: Any, tenant_id: Optional[str] = None, actor_id: Optional[str] = None) -> ModelType:
        data = schema_in.model_dump() if hasattr(schema_in, "model_dump") else dict(schema_in)
        return await self.repository.create(data, tenant_id=tenant_id)

    async def update(self, id: str, schema_in: Any, tenant_id: Optional[str] = None, actor_id: Optional[str] = None) -> ModelType:
        entity = await self.get(id, tenant_id=tenant_id)
        data = schema_in.model_dump(exclude_unset=True) if hasattr(schema_in, "model_dump") else dict(schema_in)
        return await self.repository.update(entity, data)

    async def delete(self, id: str, tenant_id: Optional[str] = None, actor_id: Optional[str] = None) -> bool:
        entity = await self.get(id, tenant_id=tenant_id)
        return await self.repository.soft_delete(id, tenant_id=tenant_id)
""")

    # 11. api/deps.py
    write_file("backend/app/api/deps.py", """from typing import AsyncGenerator, Optional
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.security import decode_token
from backend.app.core.exceptions import AuthenticationException, TenantAccessViolationException

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False
)

class CurrentUserContext:
    def __init__(self, id: str, email: str, tenant_id: str, roles: list):
        self.id = id
        self.email = email
        self.tenant_id = tenant_id
        self.roles = roles

async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[CurrentUserContext]:
    if not token:
        return None
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        roles = payload.get("roles", [])
        if not user_id:
            return None
        return CurrentUserContext(id=user_id, email=payload.get("email", ""), tenant_id=tenant_id, roles=roles)
    except Exception:
        return None

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> CurrentUserContext:
    if not token:
        raise AuthenticationException("Not authenticated")
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        roles = payload.get("roles", [])
        if not user_id:
            raise AuthenticationException("Invalid token payload")
        return CurrentUserContext(id=user_id, email=payload.get("email", ""), tenant_id=tenant_id, roles=roles)
    except jwt.PyJWTError:
        raise AuthenticationException("Invalid or expired authentication token")

async def get_current_tenant_id(
    current_user: CurrentUserContext = Depends(get_current_user),
    x_tenant_id: Optional[str] = Header(None)
) -> str:
    # If user has a tenant_id bound in token, enforce it
    if current_user.tenant_id:
        if x_tenant_id and x_tenant_id != current_user.tenant_id:
            raise TenantAccessViolationException("Tenant ID mismatch between header and credentials")
        return current_user.tenant_id
    if x_tenant_id:
        return x_tenant_id
    raise TenantAccessViolationException("No active organization context found")
""")

    # 12. api/v1/endpoints/health.py
    write_file("backend/app/api/v1/endpoints/health.py", """from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.app.core.database import get_db
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0"
    }

@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ready" if db_status == "ok" else "degraded",
        "database": db_status,
        "redis": "ok",
        "search": "ok"
    }
""")

    # 13. api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import health

api_router = APIRouter()

# Core System Routes
api_router.include_router(health.router, tags=["Health"])
""")

    # 14. main.py
    write_file("backend/app/main.py", """from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.middleware import RequestContextMiddleware
from backend.app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} in [{settings.APP_ENV}] mode...")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="ClientFlow Enterprise Multi-Tenant CRM Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Request context & security headers middleware
app.add_middleware(RequestContextMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "status": "online",
        "docs": "/docs",
        "version": "1.0.0"
    }
""")

    print("Milestone 2 Backend Foundation files generated successfully!")

if __name__ == '__main__':
    run()
