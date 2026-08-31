import uuid
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
