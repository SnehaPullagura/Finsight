import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CalendarEvent(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "calendar_events"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meeting_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_all_day: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Associated CRM entity
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    
    organizer_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    organizer: Mapped["backend.app.models.auth.User"] = relationship("backend.app.models.auth.User")
    attendees: Mapped[List["EventAttendee"]] = relationship("EventAttendee", back_populates="event", cascade="all, delete-orphan")

class EventAttendee(UUIDModel, TimestampMixin):
    __tablename__ = "event_attendees"

    event_id: Mapped[str] = mapped_column(String(36), ForeignKey("calendar_events.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="accepted", nullable=False) # accepted, declined, tentative, needs_action
    is_organizer: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    event: Mapped["CalendarEvent"] = relationship("CalendarEvent", back_populates="attendees")
