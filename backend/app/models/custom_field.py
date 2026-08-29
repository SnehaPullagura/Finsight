import uuid
from typing import List, Optional
from sqlalchemy import Boolean, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.models.base import Base, UUIDModel, TimestampMixin, TenantMixin

class CustomFieldDefinition(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "custom_field_definitions"

    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # contact, company, lead, deal, ticket
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    field_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    field_type: Mapped[str] = mapped_column(String(50), nullable=False) # text, number, boolean, date, datetime, select, multiselect, currency, url
    options_list: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
