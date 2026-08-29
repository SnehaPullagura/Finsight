import pytest
from datetime import datetime
from backend.app.schemas.audit import AuditLogCreate, AuditLogResponse

def test_audit_log_schema_validation():
    create_schema = AuditLogCreate(
        action="UPDATE",
        entity_type="deal",
        entity_id="deal_987654",
        before_snapshot={"stage": "Qualification", "amount": 10000},
        after_snapshot={"stage": "Proposal Sent", "amount": 12500},
        ip_address="192.168.1.100"
    )
    assert create_schema.action == "UPDATE"
    assert create_schema.entity_type == "deal"
    assert create_schema.before_snapshot["stage"] == "Qualification"
    assert create_schema.after_snapshot["stage"] == "Proposal Sent"

def test_audit_log_response_serialization():
    resp = AuditLogResponse(
        id="aud_12345",
        tenant_id="ten_999",
        actor_id="usr_admin",
        actor_email="admin@clientflow.io",
        action="STAGE_CHANGE",
        entity_type="lead",
        entity_id="lead_555",
        before_snapshot={"status": "new"},
        after_snapshot={"status": "contacted"},
        ip_address="10.0.0.1",
        timestamp=datetime.utcnow()
    )
    assert resp.id == "aud_12345"
    assert resp.actor_email == "admin@clientflow.io"
    assert resp.action == "STAGE_CHANGE"
