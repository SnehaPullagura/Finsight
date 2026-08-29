import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Ticket(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "support_tickets"

    ticket_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False, index=True) # urgent, high, medium, low
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False, index=True) # open, pending, in_progress, resolved, closed
    category: Mapped[str] = mapped_column(String(50), default="technical", nullable=False, index=True)
    
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    assigned_to_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    sla_due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_escalated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    contact: Mapped[Optional["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact")
    company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")
    assigned_to: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User", foreign_keys=[assigned_to_id])
    comments: Mapped[List["TicketComment"]] = relationship("TicketComment", back_populates="ticket", cascade="all, delete-orphan", order_by="TicketComment.created_at.asc()")

class TicketComment(UUIDModel, TimestampMixin):
    __tablename__ = "ticket_comments"

    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("support_tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_internal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="comments")
    author: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
