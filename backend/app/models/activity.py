import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Activity(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "activities"

    # Polymorphic entity association
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # contact, company, lead, deal, ticket, proposal
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # CALL, MEETING, EMAIL, TASK, NOTE, STATUS_CHANGE, FOLLOW_UP
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Execution metadata
    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Outcomes & sentiment
    outcome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # connected, left_voicemail, no_answer, scheduled_meeting, resolved
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True) # positive, neutral, negative
    
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    user: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    participants: Mapped[List["ActivityParticipant"]] = relationship("ActivityParticipant", back_populates="activity", cascade="all, delete-orphan")

class ActivityParticipant(UUIDModel):
    __tablename__ = "activity_participants"

    activity_id: Mapped[str] = mapped_column(String(36), ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True)
    participant_type: Mapped[str] = mapped_column(String(50), nullable=False) # contact, user, lead
    participant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(50), default="attendee", nullable=False) # host, attendee, organizer

    activity: Mapped["Activity"] = relationship("Activity", back_populates="participants")
