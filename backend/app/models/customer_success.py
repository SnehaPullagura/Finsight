import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CustomerSuccessPlan(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "customer_success_plans"

    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    status: Mapped[str] = mapped_column(String(50), default="onboarding", nullable=False, index=True) # onboarding, active, at_risk, churned
    health_score: Mapped[int] = mapped_column(Integer, default=80, nullable=False, index=True) # 0 to 100
    health_grade: Mapped[str] = mapped_column(String(20), default="good", nullable=False) # good, warning, critical
    
    target_renewal_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    renewal_value: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    churn_risk_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    goals: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    company: Mapped["backend.app.models.company.Company"] = relationship("backend.app.models.company.Company")
    owner: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    milestones: Mapped[List["OnboardingMilestone"]] = relationship("OnboardingMilestone", back_populates="plan", cascade="all, delete-orphan", order_by="OnboardingMilestone.created_at.asc()")

class OnboardingMilestone(UUIDModel, TimestampMixin):
    __tablename__ = "onboarding_milestones"

    plan_id: Mapped[str] = mapped_column(String(36), ForeignKey("customer_success_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    plan: Mapped["CustomerSuccessPlan"] = relationship("CustomerSuccessPlan", back_populates="milestones")
