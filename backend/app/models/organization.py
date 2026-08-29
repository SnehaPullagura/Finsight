import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Organization(UUIDModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    plan_tier: Mapped[str] = mapped_column(String(50), default="enterprise", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    members: Mapped[List["OrganizationMember"]] = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    teams: Mapped[List["Team"]] = relationship("Team", back_populates="organization", cascade="all, delete-orphan")
    departments: Mapped[List["Department"]] = relationship("Department", back_populates="organization", cascade="all, delete-orphan")
    invitations: Mapped[List["OrganizationInvitation"]] = relationship("OrganizationInvitation", back_populates="organization", cascade="all, delete-orphan")

class OrganizationMember(UUIDModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "organization_members"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False) # active, suspended, invited

    organization: Mapped["Organization"] = relationship("Organization", back_populates="members")
    user: Mapped["backend.app.models.auth.User"] = relationship("backend.app.models.auth.User")
    role: Mapped[Optional["backend.app.models.auth.Role"]] = relationship("backend.app.models.auth.Role")

    __table_args__ = (UniqueConstraint("organization_id", "user_id", name="uq_org_member"),)

class Team(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    leader_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="teams", foreign_keys=["Team.tenant_id"])
    members: Mapped[List["TeamMember"]] = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")

class TeamMember(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "team_members"

    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    team: Mapped["Team"] = relationship("Team", back_populates="members")
    user: Mapped["backend.app.models.auth.User"] = relationship("backend.app.models.auth.User")

    __table_args__ = (UniqueConstraint("team_id", "user_id", name="uq_team_member"),)

class Department(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    head_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="departments", foreign_keys=["Department.tenant_id"])

class OrganizationInvitation(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "organization_invitations"

    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    role_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False) # pending, accepted, revoked

    organization: Mapped["Organization"] = relationship("Organization", back_populates="invitations", foreign_keys=["OrganizationInvitation.tenant_id"])
