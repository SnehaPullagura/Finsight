import datetime
from datetime import timezone, date
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, func
from backend.app.transactions.models import Transaction, TransactionSplit, TransactionType, TransactionStatus
from backend.app.transactions.schemas import TransactionCreate, TransactionUpdate, TransactionSearchFilter
from backend.app.accounts.models import FinancialAccount, AccountBalanceHistory
from backend.app.accounts.service import AccountService
from backend.app.core.exceptions import ResourceNotFoundException, FinSightException

class TransactionService:
    @staticmethod
    async def create_transaction(db: AsyncSession, user_id: int, data: TransactionCreate) -> Transaction:
        # Validate account ownership
        account = await AccountService.get_account(db, user_id, data.account_id)
        
        # Calculate impact on account balance
        balance_delta = 0.0
        if data.transaction_type in (TransactionType.INCOME, TransactionType.REFUND, TransactionType.INTEREST):
            balance_delta = data.amount
        elif data.transaction_type in (TransactionType.EXPENSE, TransactionType.FEE):
            balance_delta = -data.amount
        elif data.transaction_type == TransactionType.TRANSFER:
            balance_delta = -data.amount
        
        account.current_balance += balance_delta
        account.available_balance += balance_delta
        
        tx = Transaction(
            user_id=user_id,
            account_id=data.account_id,
            category_id=data.category_id,
            amount=data.amount,
            transaction_type=data.transaction_type,
            transaction_date=data.transaction_date,
            description=data.description,
            raw_description=data.raw_description or data.description,
            merchant_name=data.merchant_name or data.description.split()[0] if data.description else "Unknown",
            status=data.status,
            is_recurring=data.is_recurring,
            is_discretionary=data.is_discretionary,
            confidence_score=1.0,
            is_user_confirmed=True,
            tags=data.tags,
            notes=data.notes,
            transfer_account_id=data.transfer_account_id
        )
        db.add(tx)
        await db.flush()
        
        # Handle splits if provided
        if data.splits:
            split_total = sum(s.amount for s in data.splits)
            if abs(split_total - data.amount) > 0.01:
                raise FinSightException(detail="Sum of transaction splits must equal total transaction amount.")
            for s in data.splits:
                split = TransactionSplit(
                    transaction_id=tx.id,
                    category_id=s.category_id,
                    amount=s.amount,
                    notes=s.notes
                )
                db.add(split)
        
        # Record balance history
        history = AccountBalanceHistory(
            account_id=account.id,
            balance=account.current_balance,
            snapshot_date=datetime.datetime.now(timezone.utc),
            change_reason=f"tx_{tx.id}_{data.transaction_type.value}"
        )
        db.add(history)
        
        # Handle transfer counterpart
        if data.transaction_type == TransactionType.TRANSFER and data.transfer_account_id:
            transfer_acc = await AccountService.get_account(db, user_id, data.transfer_account_id)
            transfer_acc.current_balance += data.amount
            transfer_acc.available_balance += data.amount
            
            counter_history = AccountBalanceHistory(
                account_id=transfer_acc.id,
                balance=transfer_acc.current_balance,
                snapshot_date=datetime.datetime.now(timezone.utc),
                change_reason=f"transfer_in_from_tx_{tx.id}"
            )
            db.add(counter_history)
        
        await db.commit()
        await db.refresh(tx)
        return tx

    @staticmethod
    async def list_transactions(
        db: AsyncSession, user_id: int, filters: TransactionSearchFilter
    ) -> Tuple[List[Transaction], int]:
        query = select(Transaction).where(Transaction.user_id == user_id)
        
        if filters.account_id:
            query = query.where(Transaction.account_id == filters.account_id)
        if filters.category_id:
            query = query.where(Transaction.category_id == filters.category_id)
        if filters.transaction_type:
            query = query.where(Transaction.transaction_type == filters.transaction_type)
        if filters.start_date:
            query = query.where(Transaction.transaction_date >= filters.start_date)
        if filters.end_date:
            query = query.where(Transaction.transaction_date <= filters.end_date)
        if filters.min_amount is not None:
            query = query.where(Transaction.amount >= filters.min_amount)
        if filters.max_amount is not None:
            query = query.where(Transaction.amount <= filters.max_amount)
        if filters.is_recurring is not None:
            query = query.where(Transaction.is_recurring == filters.is_recurring)
        if filters.search:
            s = f"%{filters.search.lower()}%"
            query = query.where(
                or_(
                    func.lower(Transaction.description).like(s),
                    func.lower(Transaction.merchant_name).like(s),
                    func.lower(Transaction.tags).like(s)
                )
            )
        
        count_stmt = select(func.count()).select_from(query.subquery())
        total_count = (await db.execute(count_stmt)).scalar() or 0
        
        query = query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc())
        query = query.offset(filters.offset).limit(filters.limit)
        
        result = await db.execute(query)
        return list(result.scalars().all()), total_count

    @staticmethod
    async def get_transaction(db: AsyncSession, user_id: int, tx_id: int) -> Transaction:
        stmt = select(Transaction).where(
            Transaction.id == tx_id,
            Transaction.user_id == user_id
        )
        result = await db.execute(stmt)
        tx = result.scalar_one_or_none()
        if not tx:
            raise ResourceNotFoundException("Transaction", tx_id)
        return tx

    @staticmethod
    async def update_transaction(
        db: AsyncSession, user_id: int, tx_id: int, data: TransactionUpdate
    ) -> Transaction:
        tx = await TransactionService.get_transaction(db, user_id, tx_id)
        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(tx, k, v)
        tx.is_user_confirmed = True
        await db.commit()
        await db.refresh(tx)
        return tx

    @staticmethod
    async def delete_transaction(db: AsyncSession, user_id: int, tx_id: int) -> bool:
        tx = await TransactionService.get_transaction(db, user_id, tx_id)
        # Reverse balance impact
        account = await AccountService.get_account(db, user_id, tx.account_id)
        if tx.transaction_type in (TransactionType.INCOME, TransactionType.REFUND, TransactionType.INTEREST):
            account.current_balance -= tx.amount
        elif tx.transaction_type in (TransactionType.EXPENSE, TransactionType.FEE, TransactionType.TRANSFER):
            account.current_balance += tx.amount
        
        await db.delete(tx)
        await db.commit()
        return True
