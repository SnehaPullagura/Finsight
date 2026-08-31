# ClientFlow CRM — Security Architecture & Threat Model

## 1. Authentication & Session Security
- **Password Hashing**: Argon2id with memory-hard parameters (fallback to Bcrypt).
- **JWT Cryptography**: Signed with HMAC-SHA256, strictly validated `exp`, `sub`, `tenant_id`, and `roles` claims.
- **Two-Factor Authentication**: RFC 6238 TOTP with QR provisioning and backup recovery codes.

## 2. Multi-Tenant Isolation Model
- Hard database-level tenant isolation enforced via `TenantMixin` and repository query filters.
- Middleware validates tenant access permissions against authenticated user's organization memberships.

## 3. Defense-in-Depth Measures
- OWASP Top 10 mitigation:
  - Strict input sanitization via Pydantic v2.
  - SQL Injection prevention through parameterized SQLAlchemy ORM queries.
  - Security headers: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.
  - Rate limiting & request tracing via unique request correlation IDs (`X-Request-ID`).
