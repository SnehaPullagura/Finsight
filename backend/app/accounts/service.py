import datetime
from datetime import timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.app.accounts.models import FinancialAccount, AccountBalanceHistory, AccountStatus
from backend.app.accounts.schemas import AccountCreate, AccountUpdate, AccountReconcileRequest
from backend.app.core.masking import mask_account_number
from backend.app.core.exceptions import ResourceNotFoundException

class AccountService:
    @staticmethod
    async def create_account(db: AsyncSession, user_id: int, data: AccountCreate) -> FinancialAccount:
        masked_num = mask_account_number(data.account_number or "0000")
        
        if data.is_primary:
            await db.execute(
                update(FinancialAccount)
                .where(FinancialAccount.user_id == user_id)
                .values(is_primary=False)
            )
        
        account = FinancialAccount(
            user_id=user_id,
            name=data.name,
            account_type=data.account_type,
            account_number_masked=masked_num,
            institution_name=data.institution_name or "Manual",
            currency=data.currency,
            current_balance=data.current_balance,
            available_balance=data.current_balance,
            credit_limit=data.credit_limit,
            interest_rate=data.interest_rate,
            is_primary=data.is_primary,
            status=AccountStatus.ACTIVE,
            notes=data.notes
        )
        db.add(account)
        await db.flush()
        
        history = AccountBalanceHistory(
            account_id=account.id,
            balance=data.current_balance,
            snapshot_date=datetime.datetime.now(timezone.utc),
            change_reason="initial_creation"
        )
        db.add(history)
        await db.commit()
        await db.refresh(account)
        return account

    @staticmethod
    async def list_accounts(db: AsyncSession, user_id: int) -> List[FinancialAccount]:
        stmt = select(FinancialAccount).where(
            FinancialAccount.user_id == user_id,
            FinancialAccount.status != AccountStatus.ARCHIVED
        ).order_by(FinancialAccount.is_primary.desc(), FinancialAccount.name.asc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_account(db: AsyncSession, user_id: int, account_id: int) -> FinancialAccount:
        stmt = select(FinancialAccount).where(
            FinancialAccount.id == account_id,
            FinancialAccount.user_id == user_id
        )
        result = await db.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            raise ResourceNotFoundException("Financial Account", account_id)
        return account

    @staticmethod
    async def update_account(db: AsyncSession, user_id: int, account_id: int, data: AccountUpdate) -> FinancialAccount:
        account = await AccountService.get_account(db, user_id, account_id)
        update_dict = data.model_dump(exclude_unset=True)
        if update_dict.get("is_primary"):
            await db.execute(
                update(FinancialAccount)
                .where(FinancialAccount.user_id == user_id)
                .values(is_primary=False)
            )
        for k, v in update_dict.items():
            setattr(account, k, v)
        if "current_balance" in update_dict and update_dict["current_balance"] is not None:
            account.available_balance = update_dict["current_balance"]
            history = AccountBalanceHistory(
                account_id=account.id,
                balance=account.current_balance,
                snapshot_date=datetime.datetime.now(timezone.utc),
                change_reason="manual_update"
            )
            db.add(history)
        await db.commit()
        await db.refresh(account)
        return account

    @staticmethod
    async def reconcile_account(
        db: AsyncSession, user_id: int, account_id: int, data: AccountReconcileRequest
    ) -> FinancialAccount:
        account = await AccountService.get_account(db, user_id, account_id)
        diff = data.actual_balance - account.current_balance
        account.current_balance = data.actual_balance
        account.available_balance = data.actual_balance
        account.last_reconciled_at = datetime.datetime.now(timezone.utc)
        
        history = AccountBalanceHistory(
            account_id=account.id,
            balance=account.current_balance,
            snapshot_date=account.last_reconciled_at,
            change_reason=f"reconciliation (adjustment: {diff:+.2f})"
        )
        db.add(history)
        await db.commit()
        await db.refresh(account)
        return account

    @staticmethod
    async def delete_account(db: AsyncSession, user_id: int, account_id: int) -> bool:
        account = await AccountService.get_account(db, user_id, account_id)
        account.status = AccountStatus.ARCHIVED
        await db.commit()
        return True
