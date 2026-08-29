from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional, Union
import jwt
from passlib.context import CryptContext
import pyotp
import secrets
from backend.app.core.config import settings
from backend.app.core.exceptions import AuthenticationException

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
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "tenant_id": str(tenant_id) if tenant_id else None,
        "roles": roles or [],
        "iat": now
    }
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(
    subject: Union[str, Any],
    tenant_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "tenant_id": str(tenant_id) if tenant_id else None,
        "jti": secrets.token_hex(16),
        "iat": now
    }
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AuthenticationException("Authorization token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationException("Invalid authorization token")

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def get_totp_uri(secret: str, email: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.APP_NAME)

def verify_totp_code(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
