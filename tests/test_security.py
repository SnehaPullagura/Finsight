import pytest
from datetime import timedelta
from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_totp_secret,
    get_totp_uri,
    verify_totp_code
)
import pyotp

def test_password_hashing():
    raw_pass = 'SecureP@ssw0rd123!'
    hashed = get_password_hash(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password('WrongPassword', hashed) is False

def test_access_token_creation_and_decoding():
    user_id = 'usr_123456'
    tenant_id = 'ten_abcdef'
    roles = ['admin', 'sales_manager']
    token = create_access_token(subject=user_id, tenant_id=tenant_id, roles=roles, expires_delta=timedelta(minutes=15))
    assert isinstance(token, str)
    payload = decode_token(token)
    assert payload['sub'] == user_id
    assert payload['tenant_id'] == tenant_id
    assert payload['roles'] == roles
    assert payload['type'] == 'access'

def test_refresh_token_creation_and_decoding():
    user_id = 'usr_987654'
    tenant_id = 'ten_fedcba'
    token = create_refresh_token(subject=user_id, tenant_id=tenant_id)
    assert isinstance(token, str)
    payload = decode_token(token)
    assert payload['sub'] == user_id
    assert payload['tenant_id'] == tenant_id
    assert payload['type'] == 'refresh'
    assert 'jti' in payload

def test_totp_workflow():
    secret = generate_totp_secret()
    assert isinstance(secret, str)
    assert len(secret) >= 16
    uri = get_totp_uri(secret, 'user@clientflow.internal')
    assert 'otpauth://totp/' in uri
    
    totp = pyotp.TOTP(secret)
    current_code = totp.now()
    assert verify_totp_code(secret, current_code) is True
    assert verify_totp_code(secret, '000000') is False
