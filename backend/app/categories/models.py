import enum
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.database.base import Base, TimestampMixin

class CategoryGroup(str, enum.Enum):
    INCOME = "income"
    ESSENTIAL_EXPENSE = "essential_expense"
    DISCRETIONARY_EXPENSE = "discretionary_expense"
    SAVINGS_INVESTMENT = "savings_investment"
    DEBT_EMI = "debt_emi"
    TRANSFER = "transfer"

class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    group: Mapped[CategoryGroup] = mapped_column(SQLEnum(CategoryGroup), nullable=False, index=True)
    icon: Mapped[str] = mapped_column(String(64), default="Tag", nullable=False)
    color: Mapped[str] = mapped_column(String(16), default="#6366F1", nullable=False)
    is_tax_deductible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_system_default: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="category")
    budgets: Mapped[List["Budget"]] = relationship("Budget", back_populates="category")
