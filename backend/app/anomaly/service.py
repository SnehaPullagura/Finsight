import datetime
from datetime import date, timezone
from typing import List
from collections import defaultdict
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from backend.app.anomaly.models import FinancialAnomaly, AnomalyType
from backend.app.transactions.models import Transaction, TransactionType
from backend.app.categories.models import Category
from backend.app.core.exceptions import ResourceNotFoundException

class AnomalyDetectionEngine:
    @staticmethod
    async def scan_for_anomalies(db: AsyncSession, user_id: int) -> List[FinancialAnomaly]:
        # Fetch user's expense transactions
        stmt = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == TransactionType.EXPENSE
        ).order_by(Transaction.transaction_date.desc()).limit(200)
        res = await db.execute(stmt)
        transactions = list(res.scalars().all())
        
        if len(transactions) < 5:
            return []
        
        amounts = [t.amount for t in transactions]
        mean_amt = np.mean(amounts)
        std_amt = np.std(amounts) if len(amounts) > 1 else 1.0
        
        anomalies_detected = []
        for t in transactions[:30]:
            # Check if anomaly record already exists
            chk = await db.execute(
                select(FinancialAnomaly).where(FinancialAnomaly.transaction_id == t.id)
            )
            if chk.scalar_one_or_none():
                continue
            
            # Anomaly rule 1: Z-score > 2.5 on transaction amount
            z_score = (t.amount - mean_amt) / (std_amt + 1e-5)
            if z_score > 2.5:
                score = min(0.98, 0.70 + (z_score / 10.0))
                severity = "high" if z_score > 4.0 else "medium"
                explanation = f"Transaction amount ₹{t.amount:,.2f} is significantly higher than your typical average of ₹{mean_amt:,.2f}."
                anomaly = FinancialAnomaly(
                    user_id=user_id,
                    transaction_id=t.id,
                    anomaly_type=AnomalyType.UNUSUAL_AMOUNT,
                    anomaly_score=score,
                    severity=severity,
                    explanation=explanation
                )
                db.add(anomaly)
                anomalies_detected.append(anomaly)
        
        if anomalies_detected:
            await db.commit()
            
        # Return all unacknowledged anomalies
        list_stmt = select(FinancialAnomaly).where(
            FinancialAnomaly.user_id == user_id
        ).order_by(FinancialAnomaly.created_at.desc()).limit(20)
        list_res = await db.execute(list_stmt)
        return list(list_res.scalars().all())

    @staticmethod
    async def acknowledge_anomaly(
        db: AsyncSession, user_id: int, anomaly_id: int, is_false_positive: bool
    ) -> FinancialAnomaly:
        stmt = select(FinancialAnomaly).where(
            FinancialAnomaly.id == anomaly_id,
            FinancialAnomaly.user_id == user_id
        )
        res = await db.execute(stmt)
        anomaly = res.scalar_one_or_none()
        if not anomaly:
            raise ResourceNotFoundException("Anomaly", anomaly_id)
        anomaly.is_acknowledged = True
        anomaly.is_false_positive = is_false_positive
        await db.commit()
        await db.refresh(anomaly)
        return anomaly
