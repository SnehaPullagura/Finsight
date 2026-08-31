import datetime
from datetime import date, timezone
from typing import List
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.recurring.models import RecurringPayment, RecurringCadence
from backend.app.recurring.schemas import RecurringPaymentCreate, RecurringCalendarEvent
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.categories.models import Category

class RecurringService:
    @staticmethod
    async def create_recurring(db: AsyncSession, user_id: int, data: RecurringPaymentCreate) -> RecurringPayment:
        rec = RecurringPayment(
            user_id=user_id,
            account_id=data.account_id,
            category_id=data.category_id,
            merchant_name=data.merchant_name,
            amount=data.amount,
            cadence=data.cadence,
            next_expected_date=data.next_expected_date,
            last_payment_date=data.last_payment_date,
            is_active=True,
            is_auto_detected=False
        )
        db.add(rec)
        await db.commit()
        await db.refresh(rec)
        return rec

    @staticmethod
    async def list_recurring(db: AsyncSession, user_id: int) -> List[RecurringPayment]:
        stmt = select(RecurringPayment).where(
            RecurringPayment.user_id == user_id,
            RecurringPayment.is_active == True
        ).order_by(RecurringPayment.next_expected_date.asc())
        res = await db.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def detect_recurring(db: AsyncSession, user_id: int) -> List[RecurringPayment]:
        # Group expense transactions by merchant and similar amounts
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).order_by(Transaction.transaction_date.desc()).limit(300)
        res = await db.execute(stmt)
        txs = list(res.scalars().all())
        
        merchant_groups = defaultdict(list)
        for t in txs:
            if t.merchant_name:
                merchant_groups[t.merchant_name.lower()].append(t)
        
        detected = []
        for m_name, group in merchant_groups.items():
            if len(group) >= 2:
                # Check intervals
                dates = sorted([t.transaction_date for t in group])
                diffs = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                avg_diff = sum(diffs) / len(diffs) if diffs else 0
                
                # Check monthly pattern (25 - 35 days)
                if 25 <= avg_diff <= 35:
                    latest = dates[-1]
                    next_date = latest + datetime.timedelta(days=30)
                    # Check if already saved
                    chk = await db.execute(
                        select(RecurringPayment).where(
                            RecurringPayment.user_id == user_id,
                            RecurringPayment.merchant_name == group[0].merchant_name
                        )
                    )
                    existing = chk.scalar_one_or_none()
                    if not existing:
                        rec = RecurringPayment(
                            user_id=user_id,
                            account_id=group[0].account_id,
                            category_id=group[0].category_id,
                            merchant_name=group[0].merchant_name,
                            amount=group[0].amount,
                            cadence=RecurringCadence.MONTHLY,
                            next_expected_date=next_date,
                            last_payment_date=latest,
                            is_active=True,
                            is_auto_detected=True
                        )
                        db.add(rec)
                        detected.append(rec)
        if detected:
            await db.commit()
        return await RecurringService.list_recurring(db, user_id)

    @staticmethod
    async def get_payment_calendar(db: AsyncSession, user_id: int, days_ahead: int = 60) -> List[RecurringCalendarEvent]:
        recurring = await RecurringService.list_recurring(db, user_id)
        events = []
        today = date.today()
        horizon = today + datetime.timedelta(days=days_ahead)
        
        for r in recurring:
            cat_name = "Subscription / Bill"
            if r.category_id:
                c_res = await db.execute(select(Category).where(Category.id == r.category_id))
                c = c_res.scalar_one_or_none()
                if c:
                    cat_name = c.name
            
            curr_date = r.next_expected_date
            while curr_date <= horizon:
                events.append(RecurringCalendarEvent(
                    merchant_name=r.merchant_name,
                    amount=r.amount,
                    expected_date=curr_date,
                    cadence=r.cadence.value,
                    category_name=cat_name
                ))
                if r.cadence == RecurringCadence.MONTHLY:
                    curr_date = curr_date + datetime.timedelta(days=30)
                elif r.cadence == RecurringCadence.WEEKLY:
                    curr_date = curr_date + datetime.timedelta(days=7)
                elif r.cadence == RecurringCadence.YEARLY:
                    curr_date = curr_date + datetime.timedelta(days=365)
                else:
                    break
        return sorted(events, key=lambda x: x.expected_date)
