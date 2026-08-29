import uuid
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Contact(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "contacts"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    secondary_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    mobile_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    title: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    lifecycle_stage: Mapped[str] = mapped_column(String(50), default="lead", nullable=False, index=True) # lead, mql, sql, opportunity, customer, other
    lead_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    twitter_handle: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    is_do_not_call: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_do_not_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company", back_populates="contacts")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
