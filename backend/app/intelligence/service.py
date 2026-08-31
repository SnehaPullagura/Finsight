import re
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.categories.models import Category, CategoryGroup
from backend.app.categories.service import CategoryService
from backend.app.intelligence.schemas import CategorizationResponse
from backend.app.intelligence.models import CategorizationFeedback

MERCHANT_RULES = {
    # Groceries
    r"(swiggy instamart|blinkit|zepto|bigbasket|dmart|spencer|reliance fresh|nature basket|grofers)": ("Groceries & Supermarket", "Groceries"),
    # Food & Dining
    r"(swiggy|zomato|starbucks|mcdonalds|kfc|dominos|pizza hut|subway|burger king|chaayos|blue tokai)": ("Dining Out & Cafes", "Dining"),
    # Commute & Fuel
    r"(uber|ola|rapido|blusmart|petrol|hpcl|bpcl|ioc|shell|fuel|metro)": ("Fuel & Commute", "Commute"),
    # Utilities & Telecom
    r"(airtel|jio|vi |vodafone|tatapower|bescom|electricity|water board|act fibernet|broadband)": ("Utilities & Electricity", "Utilities"),
    # Shopping
    r"(amazon|flipkart|myntra|ajio|zara|h&m|ikea|nykaa|tata cliq|croma|reliance digital)": ("Shopping & Apparel", "Shopping"),
    # Entertainment & Subscriptions
    r"(netflix|spotify|hotstar|prime video|youtube premium|apple\.com|playstation|steam|pvr|inox)": ("Subscriptions & Streaming", "Entertainment"),
    # Healthcare
    r"(apollo|pharmeasy|1mg|netmeds|max healthcare|fortis|practo|dentist|hospital|clinic)": ("Healthcare & Pharmacy", "Healthcare"),
    # EMIs & Loans
    r"(hdfc loan|icici loan|bajaj finance|cred|sbi cards|home loan emi|car loan emi)": ("Home Loan EMI", "Debt EMI"),
    # Investments
    r"(zerodha|groww|kuvera|upstox|uti mf|hdfc mf|sbi mutual|etmoney|indmoney|ppf|nps)": ("Mutual Funds & SIP", "Investments"),
    # Income
    r"(salary|payroll|direct deposit|freelance|client payment|consulting fee|dividend)": ("Salary & Wages", "Salary")
}

class TransactionIntelligenceService:
    @staticmethod
    def normalize_text(text: str) -> str:
        if not text:
            return ""
        # Remove transaction codes like UPI/REF/NEFT/POS
        clean = re.sub(r"(?i)(upi|pos|neft|rtgs|imps|ref|txn|inb|atm|wdr|mb)", " ", text)
        clean = re.sub(r"[\d/\-_@]+", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip().lower()
        return clean

    @staticmethod
    def extract_merchant(text: str) -> str:
        clean = text.strip()
        for pattern, (cat, merch_hint) in MERCHANT_RULES.items():
            match = re.search(pattern, clean, re.IGNORECASE)
            if match:
                return match.group(0).title()
        words = clean.split()
        return words[0].title() if words else "Unknown"

    @staticmethod
    async def categorize(db: AsyncSession, description: str, amount: Optional[float] = None) -> CategorizationResponse:
        desc_lower = description.lower()
        target_category_name = "Shopping & Apparel"
        merchant = TransactionIntelligenceService.extract_merchant(description)
        confidence = 0.65
        is_recurring = False

        # 1. Match Rules
        for pattern, (cat_name, m_hint) in MERCHANT_RULES.items():
            if re.search(pattern, desc_lower):
                target_category_name = cat_name
                confidence = 0.94
                if "subscription" in cat_name.lower() or "emi" in cat_name.lower() or "rent" in cat_name.lower():
                    is_recurring = True
                break

        # 2. Check user feedback history
        fb_stmt = select(CategorizationFeedback).where(
            CategorizationFeedback.raw_text == desc_lower
        ).order_by(CategorizationFeedback.id.desc()).limit(1)
        fb_res = await db.execute(fb_stmt)
        fb = fb_res.scalar_one_or_none()
        if fb:
            cat_stmt = select(Category).where(Category.id == fb.corrected_category_id)
            c_res = await db.execute(cat_stmt)
            cat_db = c_res.scalar_one_or_none()
            if cat_db:
                return CategorizationResponse(
                    category_id=cat_db.id,
                    category_name=cat_db.name,
                    category_group=cat_db.group.value,
                    merchant_name=fb.merchant_name or merchant,
                    confidence_score=0.99,
                    is_recurring_predicted=is_recurring,
                    category=cat_db
                )

        # Look up category in database
        cat_stmt = select(Category).where(Category.name == target_category_name)
        cat_res = await db.execute(cat_stmt)
        category = cat_res.scalar_one_or_none()
        
        if not category:
            await CategoryService.seed_defaults(db)
            cat_stmt = select(Category).where(Category.name == target_category_name)
            cat_res = await db.execute(cat_stmt)
            category = cat_res.scalar_one_or_none()
            if not category:
                fallback_res = await db.execute(select(Category).limit(1))
                category = fallback_res.scalar_one()

        return CategorizationResponse(
            category_id=category.id,
            category_name=category.name,
            category_group=category.group.value,
            merchant_name=merchant,
            confidence_score=confidence,
            is_recurring_predicted=is_recurring,
            category=category
        )

    @staticmethod
    async def record_user_feedback(
        db: AsyncSession, user_id: int, transaction_id: Optional[int],
        raw_text: str, corrected_category_id: int, merchant_name: Optional[str] = None
    ) -> CategorizationFeedback:
        fb = CategorizationFeedback(
            user_id=user_id,
            transaction_id=transaction_id,
            raw_text=raw_text.lower().strip(),
            corrected_category_id=corrected_category_id,
            merchant_name=merchant_name,
            confidence=1.0,
            is_trained=False
        )
        db.add(fb)
        await db.commit()
        await db.refresh(fb)
        return fb
