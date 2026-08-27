import pytest
from backend.app.core.masking import (
    mask_account_number, mask_card_number, mask_pan_or_tax_id,
    mask_email, sanitize_audit_payload
)

def test_masking_algorithms():
    # Bank Account
    assert mask_account_number("123456789012") == "XXXX-XXXX-9012"
    assert mask_account_number("12") == "XXXX"

    # Credit Card
    assert mask_card_number("4111222233334444") == "•••• •••• •••• 4444"

    # Email
    assert mask_email("chaitanya.tech@finsight.app") == "ch***h@finsight.app"

    # Tax ID / PAN
    assert mask_pan_or_tax_id("ABCDE1234F") == "ABXXXXX4F"

    # Redact dictionary
    sensitive = {
        "user": "Chaitanya",
        "password": "SecretPassword123!",
        "token": "bearer xyz-jwt",
        "access_token": "abc-123",
        "public_data": "visible"
    }
    redacted = sanitize_audit_payload(sensitive)
    assert redacted["password"] == "[REDACTED]"
    assert redacted["token"] == "[REDACTED]"
    assert redacted["access_token"] == "[REDACTED]"
    assert redacted["public_data"] == "visible"
