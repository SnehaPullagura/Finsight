import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/integrations/models.py
    write_file("backend/app/integrations/models.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, TenantMixin

class IntegrationConnection(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "integrations_connections"

    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # stripe, twilio, sendgrid, google, microsoft, slack
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="connected", nullable=False) # connected, error, expired, disabled
    auth_type: Mapped[str] = mapped_column(String(50), default="oauth2", nullable=False) # oauth2, api_key, webhook
    credentials_encrypted: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class WebhookSubscription(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "integrations_webhook_subscriptions"

    target_url: Mapped[str] = mapped_column(String(500), nullable=False)
    secret_key: Mapped[str] = mapped_column(String(100), nullable=False)
    events: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    failure_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
""")

    # 2. backend/app/integrations/base.py & Adapters
    write_file("backend/app/integrations/base.py", """import abc
from typing import Any, Dict, Optional

class BaseIntegrationAdapter(abc.ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abc.abstractmethod
    async def test_connection(self) -> bool:
        pass

    @abc.abstractmethod
    async def sync_data(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        pass
""")

    write_file("backend/app/integrations/stripe_adapter.py", """import hmac
import hashlib
import json
from typing import Any, Dict
from backend.app.integrations.base import BaseIntegrationAdapter

class StripeIntegrationAdapter(BaseIntegrationAdapter):
    async def test_connection(self) -> bool:
        api_key = self.config.get("api_key", "")
        return bool(api_key.startswith("sk_"))

    async def sync_data(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Mock Stripe Customer / PaymentIntent creation
        return {
            "stripe_id": f"cus_mock_{data.get('id', '001')}",
            "status": "synchronized",
            "provider": "stripe",
            "entity": entity_type
        }

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        secret = self.config.get("webhook_secret", "whsec_mock")
        computed = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(computed, signature.replace("t=", "").split(",")[-1].replace("v1=", ""))
""")

    write_file("backend/app/integrations/slack_adapter.py", """from typing import Any, Dict, List
from backend.app.integrations.base import BaseIntegrationAdapter

class SlackIntegrationAdapter(BaseIntegrationAdapter):
    async def test_connection(self) -> bool:
        return bool(self.config.get("webhook_url"))

    async def sync_data(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "dispatched", "channel": self.config.get("channel", "#sales-alerts")}

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        return True

    @staticmethod
    def format_deal_won_block(deal_name: str, deal_value: float, rep_name: str, currency: str = "USD") -> Dict[str, Any]:
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": f"🎉 Deal Won: {deal_name}!"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Amount:*\n{currency} {deal_value:,.2f}"},
                        {"type": "mrkdwn", "text": f"*Owner:*\n{rep_name}"}
                    ]
                }
            ]
        }
""")

    # 3. backend/app/integrations/migration_engine.py
    write_file("backend/app/integrations/migration_engine.py", """import csv
import io
import json
from typing import Dict, List, Tuple

class DataMigrationEngine:
    @staticmethod
    def map_and_transform_contacts(
        raw_records: List[Dict[str, str]],
        field_mappings: Dict[str, str]
    ) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        valid_contacts = []
        rejected_records = []

        for row in raw_records:
            transformed = {}
            for source_col, target_field in field_mappings.items():
                val = row.get(source_col, "").strip()
                if val:
                    transformed[target_field] = val

            # Validation
            if "email" in transformed and "@" in transformed["email"]:
                if "first_name" not in transformed:
                    transformed["first_name"] = transformed["email"].split("@")[0].capitalize()
                if "last_name" not in transformed:
                    transformed["last_name"] = "Contact"
                valid_contacts.append(transformed)
            else:
                rejected_records.append({"row": row, "reason": "Missing or invalid email address"})

        return valid_contacts, rejected_records

    @staticmethod
    def parse_csv_to_dicts(csv_text: str) -> List[Dict[str, str]]:
        reader = csv.DictReader(io.StringIO(csv_text.strip()))
        return list(reader)
""")

    # 4. backend/app/integrations/schemas.py & Endpoints
    write_file("backend/app/integrations/schemas.py", """from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ConnectionCreateRequest(BaseModel):
    provider: str
    name: str
    auth_type: str = "api_key"
    credentials: Dict[str, Any]
    settings: Optional[Dict[str, Any]] = None

class ConnectionResponse(BaseModel):
    id: str
    provider: str
    name: str
    status: str
    auth_type: str
    is_active: bool

class MigrationPreviewRequest(BaseModel):
    csv_content: str
    field_mappings: Dict[str, str]

class MigrationPreviewResponse(BaseModel):
    total_parsed: int
    valid_count: int
    rejected_count: int
    sample_valid: List[Dict[str, str]]
    sample_rejected: List[Dict[str, Any]]
""")

    write_file("backend/app/api/v1/endpoints/integrations_hub.py", """from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_tenant_id
from backend.app.schemas.integrations import (
    ConnectionCreateRequest,
    ConnectionResponse,
    MigrationPreviewRequest,
    MigrationPreviewResponse
)
from backend.app.integrations.models import IntegrationConnection
from backend.app.integrations.migration_engine import DataMigrationEngine

router = APIRouter()

@router.post("/connections", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def create_connection(
    req: ConnectionCreateRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    conn = IntegrationConnection(
        tenant_id=tenant_id,
        provider=req.provider,
        name=req.name,
        auth_type=req.auth_type,
        credentials_encrypted=req.credentials,
        settings=req.settings or {},
        status="connected",
        is_active=True
    )
    db.add(conn)
    await db.flush()
    await db.refresh(conn)
    return conn

@router.post("/migrate-preview", response_model=MigrationPreviewResponse)
async def preview_data_migration(req: MigrationPreviewRequest):
    rows = DataMigrationEngine.parse_csv_to_dicts(req.csv_content)
    valid, rejected = DataMigrationEngine.map_and_transform_contacts(rows, req.field_mappings)

    return MigrationPreviewResponse(
        total_parsed=len(rows),
        valid_count=len(valid),
        rejected_count=len(rejected),
        sample_valid=valid[:5],
        sample_rejected=rejected[:5]
    )
""")

    print("Integrations Hub & Migration Engine created.")

if __name__ == '__main__':
    run()
