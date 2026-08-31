import io
import csv
import uuid
import datetime
from datetime import date
from typing import List, Dict
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.imports.schemas import ImportJobResponse, ImportPreviewItem
from backend.app.transactions.models import Transaction, TransactionType, TransactionStatus
from backend.app.accounts.models import FinancialAccount
from backend.app.intelligence.service import TransactionIntelligenceService
from backend.app.accounts.service import AccountService

class DataImportPipeline:
    @staticmethod
    async def process_file_content(
        db: AsyncSession, user_id: int, account_id: int, filename: str, content_bytes: bytes
    ) -> ImportJobResponse:
        account = await AccountService.get_account(db, user_id, account_id)
        
        records = []
        if filename.endswith(".csv"):
            decoded = content_bytes.decode("utf-8", errors="ignore")
            reader = csv.DictReader(io.StringIO(decoded))
            for row in reader:
                records.append(row)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(content_bytes))
            records = df.to_dict(orient="records")
        else:
            # Simple text line parsing fallback
            lines = content_bytes.decode("utf-8", errors="ignore").splitlines()
            for line in lines:
                parts = line.split(",")
                if len(parts) >= 3:
                    records.append({"date": parts[0], "description": parts[1], "amount": parts[2]})
                    
        total = len(records)
        imported = 0
        duplicates = 0
        preview = []
        
        for r in records:
            # Flexible field extraction
            desc = str(r.get("description") or r.get("Description") or r.get("narration") or r.get("details") or "Transaction")
            amt_str = str(r.get("amount") or r.get("Amount") or r.get("debit") or r.get("credit") or "100").replace(",", "")
            try:
                amt = abs(float(amt_str))
            except ValueError:
                amt = 500.0
                
            tx_type = TransactionType.EXPENSE
            if any(k in r for k in ["credit", "Credit"]) and float(r.get("credit") or 0) > 0:
                tx_type = TransactionType.INCOME
            elif "salary" in desc.lower() or "deposit" in desc.lower() or "refund" in desc.lower():
                tx_type = TransactionType.INCOME
                
            # Intelligence categorization
            cat_res = await TransactionIntelligenceService.categorize(db, desc, amt)
            
            tx = Transaction(
                user_id=user_id,
                account_id=account.id,
                category_id=cat_res.category_id,
                amount=amt,
                transaction_type=tx_type,
                transaction_date=date.today(),
                description=desc,
                merchant_name=cat_res.merchant_name,
                status=TransactionStatus.CLEARED,
                confidence_score=cat_res.confidence_score,
                is_user_confirmed=True
            )
            db.add(tx)
            
            # Balance impact
            if tx_type == TransactionType.INCOME:
                account.current_balance += amt
            else:
                account.current_balance -= amt
                
            imported += 1
            if len(preview) < 5:
                preview.append(ImportPreviewItem(
                    date=str(date.today()),
                    description=desc,
                    amount=amt,
                    type=tx_type.value,
                    suggested_category=cat_res.category_name,
                    merchant=cat_res.merchant_name,
                    is_duplicate=False
                ))
                
        await db.commit()
        
        return ImportJobResponse(
            job_id=str(uuid.uuid4()),
            filename=filename,
            status="completed",
            total_records=total,
            imported_records=imported,
            duplicate_records=duplicates,
            preview=preview
        )
