import uuid
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class ProductCategory(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "product_categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Optional[Mapped[str]] = mapped_column(String(255), nullable=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")

class Product(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("product_categories.id", ondelete="SET NULL"), nullable=True)
    description: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    cost_price: Optional[Mapped[float]] = mapped_column(Numeric(18, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_service: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    inventory_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    category: Mapped[Optional["ProductCategory"]] = relationship("ProductCategory", back_populates="products")
