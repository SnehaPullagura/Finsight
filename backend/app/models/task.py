import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Task(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False, index=True) # urgent, high, medium, low
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False, index=True) # pending, in_progress, completed, cancelled
    
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Associated CRM entity
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True) # contact, company, lead, deal, ticket
    entity_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    
    assigned_to_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Recurrence & reminders
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # daily, weekly, monthly, cron
    reminder_minutes_before: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    assigned_to: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User", foreign_keys=[assigned_to_id])
    created_by: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User", foreign_keys=[created_by_id])
