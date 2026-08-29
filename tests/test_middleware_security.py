import pytest
from datetime import timedelta
from starlette.requests import Request
from starlette.responses import Response
from backend.app.core.security import create_access_token, decode_token
from backend.app.core.exceptions import AuthenticationException
from backend.app.core.middleware import RequestContextMiddleware

def test_token_expiration_handling():
    expired_token = create_access_token(
        subject="user_expired",
        expires_delta=timedelta(seconds=-3600)
    )
    with pytest.raises(AuthenticationException) as exc_info:
        decode_token(expired_token)
    assert "expired" in str(exc_info.value.detail["message"]).lower()

def test_invalid_token_handling():
    with pytest.raises(AuthenticationException) as exc_info:
        decode_token("invalid.token.string")
    assert "invalid" in str(exc_info.value.detail["message"]).lower()

@pytest.mark.asyncio
async def test_middleware_security_headers_injection():
    middleware = RequestContextMiddleware(app=None)
    
    async def dummy_call_next(request: Request) -> Response:
        return Response(content="OK", media_type="text/plain")

    # Mock ASGI request
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/v1/health",
        "headers": [(b"x-request-id", b"test-req-123"), (b"x-tenant-id", b"tenant-456")]
    }
    request = Request(scope)
    response = await middleware.dispatch(request, dummy_call_next)
    
    assert response.headers.get("X-Request-ID") == "test-req-123"
    assert "X-Response-Time-MS" in response.headers
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert response.headers.get("Permissions-Policy") == "camera=(), microphone=(), geolocation=()"
