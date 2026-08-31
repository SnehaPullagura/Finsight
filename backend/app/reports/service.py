import csv
import io
import uuid
import datetime
from datetime import date
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.reports.schemas import ReportGenerateRequest, ReportGenerateResponse
from backend.app.transactions.models import Transaction, TransactionType
from sqlalchemy import select

class ReportGeneratorService:
    @staticmethod
    async def generate_report(
        db: AsyncSession, user_id: int, req: ReportGenerateRequest
    ) -> ReportGenerateResponse:
        stmt = select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.transaction_date.desc()).limit(100)
        res = await db.execute(stmt)
        txs = list(res.scalars().all())
        
        total_in = sum(t.amount for t in txs if t.transaction_type == TransactionType.INCOME)
        total_out = sum(t.amount for t in txs if t.transaction_type == TransactionType.EXPENSE)
        
        rep_id = str(uuid.uuid4())
        filename = f"finsight_{req.report_type}_{date.today().isoformat()}.{req.format}"
        
        return ReportGenerateResponse(
            report_id=rep_id,
            report_name=filename,
            format=req.format,
            download_url=f"/api/v1/reports/download/{rep_id}",
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            summary_metrics={
                "total_inflow": round(total_in, 2),
                "total_outflow": round(total_out, 2),
                "net_savings": round(total_in - total_out, 2),
                "transaction_count": float(len(txs))
            }
        )
