import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.categories.models import Category, CategoryGroup

DEFAULT_CATEGORIES = [
    {"name": "Salary & Wages", "group": CategoryGroup.INCOME, "icon": "Briefcase", "color": "#10B981"},
    {"name": "Business & Freelance", "group": CategoryGroup.INCOME, "icon": "Laptop", "color": "#059669"},
    {"name": "Dividends & Interest", "group": CategoryGroup.INCOME, "icon": "TrendingUp", "color": "#34D399"},
    {"name": "Rental Income", "group": CategoryGroup.INCOME, "icon": "Home", "color": "#6EE7B7"},
    {"name": "Refunds & Reimbursements", "group": CategoryGroup.INCOME, "icon": "RotateCcw", "color": "#A7F3D0"},
    {"name": "Other Income", "group": CategoryGroup.INCOME, "icon": "PlusCircle", "color": "#047857"},
    
    {"name": "Housing & Rent", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Home", "color": "#EF4444"},
    {"name": "Groceries & Supermarket", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "ShoppingCart", "color": "#F97316"},
    {"name": "Utilities & Electricity", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Zap", "color": "#F59E0B"},
    {"name": "Healthcare & Pharmacy", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "HeartPulse", "color": "#EC4899"},
    {"name": "Fuel & Commute", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Fuel", "color": "#84CC16"},
    {"name": "Insurance Premiums", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "ShieldCheck", "color": "#06B6D4", "is_tax_deductible": True},
    {"name": "Education & Tuition", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "GraduationCap", "color": "#3B82F6", "is_tax_deductible": True},
    {"name": "Mobile & Internet", "group": CategoryGroup.ESSENTIAL_EXPENSE, "icon": "Wifi", "color": "#6366F1"},
    
    {"name": "Dining Out & Cafes", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Utensils", "color": "#FB923C"},
    {"name": "Food Delivery", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Bike", "color": "#F87171"},
    {"name": "Entertainment & Movies", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Film", "color": "#A855F7"},
    {"name": "Shopping & Apparel", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "ShoppingBag", "color": "#EC4899"},
    {"name": "Travel & Vacation", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Plane", "color": "#0EA5E9"},
    {"name": "Subscriptions & Streaming", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Tv", "color": "#8B5CF6"},
    {"name": "Personal Care & Grooming", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Sparkles", "color": "#D946EF"},
    {"name": "Gifts & Donations", "group": CategoryGroup.DISCRETIONARY_EXPENSE, "icon": "Gift", "color": "#14B8A6"},
    
    {"name": "Mutual Funds & SIP", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "BarChart3", "color": "#3B82F6"},
    {"name": "Fixed Deposits & RD", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "PiggyBank", "color": "#2563EB"},
    {"name": "Stocks & Equity", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "LineChart", "color": "#1D4ED8"},
    {"name": "Gold & Commodities", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "Coins", "color": "#D97706"},
    {"name": "Retirement & PPF", "group": CategoryGroup.SAVINGS_INVESTMENT, "icon": "Shield", "color": "#4F46E5", "is_tax_deductible": True},
    
    {"name": "Home Loan EMI", "group": CategoryGroup.DEBT_EMI, "icon": "Building", "color": "#DC2626", "is_tax_deductible": True},
    {"name": "Car Loan EMI", "group": CategoryGroup.DEBT_EMI, "icon": "Car", "color": "#B91C1C"},
    {"name": "Personal Loan EMI", "group": CategoryGroup.DEBT_EMI, "icon": "CreditCard", "color": "#991B1B"},
    {"name": "Credit Card Bill", "group": CategoryGroup.DEBT_EMI, "icon": "Receipt", "color": "#7F1D1D"},
    
    {"name": "Account Transfer", "group": CategoryGroup.TRANSFER, "icon": "ArrowLeftRight", "color": "#64748B"},
    {"name": "ATM Cash Withdrawal", "group": CategoryGroup.TRANSFER, "icon": "Banknote", "color": "#475569"}
]

class CategoryService:
    @staticmethod
    async def seed_defaults(db: AsyncSession):
        for cat_data in DEFAULT_CATEGORIES:
            slug = re.sub(r"[^a-z0-9]+", "-", cat_data["name"].lower()).strip("-")
            stmt = select(Category).where(Category.slug == slug)
            res = await db.execute(stmt)
            if not res.scalar_one_or_none():
                cat = Category(
                    name=cat_data["name"],
                    slug=slug,
                    group=cat_data["group"],
                    icon=cat_data.get("icon", "Tag"),
                    color=cat_data.get("color", "#6366F1"),
                    is_tax_deductible=cat_data.get("is_tax_deductible", False),
                    is_system_default=True
                )
                db.add(cat)
        await db.commit()

    @staticmethod
    async def list_categories(db: AsyncSession) -> List[Category]:
        stmt = select(Category).order_by(Category.group.asc(), Category.name.asc())
        result = await db.execute(stmt)
        categories = list(result.scalars().all())
        if not categories:
            await CategoryService.seed_defaults(db)
            result = await db.execute(stmt)
            categories = list(result.scalars().all())
        return categories
