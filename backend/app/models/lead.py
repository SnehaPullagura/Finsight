import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Lead(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "leads"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False, index=True) # new, contacted, qualified, unqualified, converted
    source: Mapped[str] = mapped_column(String(100), default="website", nullable=False, index=True)
    
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    qualification_grade: Mapped[str] = mapped_column(String(2), default="C", nullable=False) # A, B, C, D, F
    qualification_details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    
    estimated_budget: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    employee_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    intent_score: Mapped[int] = mapped_column(Integer, default=50, nullable=False) # 0 to 100
    engagement_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Conversion references
    converted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    converted_contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    converted_company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    converted_deal_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    converted_contact: Mapped[Optional["backend.app.models.contact.Contact"]] = relationship("backend.app.models.contact.Contact")
    converted_company: Mapped[Optional["backend.app.models.company.Company"]] = relationship("backend.app.models.company.Company")

class LeadScoringRule(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "lead_scoring_rules"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    criteria_type: Mapped[str] = mapped_column(String(50), nullable=False) # budget, company_size, industry, engagement, intent
    operator: Mapped[str] = mapped_column(String(20), nullable=False) # gt, gte, lt, lte, eq, in, contains
    target_value: Mapped[str] = mapped_column(String(255), nullable=False)
    score_weight: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
