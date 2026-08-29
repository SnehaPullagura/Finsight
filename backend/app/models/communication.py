import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CommunicationMessage(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "communication_messages"

    channel: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # email, sms, internal_message, webhook
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    subject: Optional[Mapped[str]] = mapped_column(String(500), nullable=True)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="sent", nullable=False, index=True) # draft, queued, sent, delivered, opened, failed
    tracking_id: Optional[Mapped[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    
    # Associated CRM entity
    entity_type: Optional[Mapped[str]] = mapped_column(String(50), nullable=True, index=True)
    entity_id: Optional[Mapped[str]] = mapped_column(String(36), nullable=True, index=True)
    
    user_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    sent_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    user: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")

class CommunicationTemplate(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "communication_templates"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="email", nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="general", nullable=False) # sales, support, marketing, onboarding
    
    subject_template: Optional[Mapped[str]] = mapped_column(String(500), nullable=True)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    available_variables: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
