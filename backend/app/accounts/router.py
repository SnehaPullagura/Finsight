from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.accounts.schemas import (
    AccountCreate, AccountUpdate, AccountResponse, BalanceHistoryResponse, AccountReconcileRequest
)
from backend.app.accounts.service import AccountService
from backend.app.accounts.models import AccountBalanceHistory
from sqlalchemy import select

router = APIRouter(prefix="/accounts", tags=["Financial Accounts"])

@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.create_account(db, current_user.id, data)

@router.get("", response_model=List[AccountResponse])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.list_accounts(db, current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.get_account(db, current_user.id, account_id)

@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    data: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.update_account(db, current_user.id, account_id, data)

@router.post("/{account_id}/reconcile", response_model=AccountResponse)
async def reconcile_account(
    account_id: int,
    data: AccountReconcileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AccountService.reconcile_account(db, current_user.id, account_id, data)

@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AccountService.delete_account(db, current_user.id, account_id)
    return {"message": "Account archived successfully"}

@router.get("/{account_id}/history", response_model=List[BalanceHistoryResponse])
async def get_balance_history(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await AccountService.get_account(db, current_user.id, account_id)
    stmt = select(AccountBalanceHistory).where(
        AccountBalanceHistory.account_id == account_id
    ).order_by(AccountBalanceHistory.snapshot_date.desc()).limit(100)
    res = await db.execute(stmt)
    return list(res.scalars().all())
