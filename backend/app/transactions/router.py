from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.transactions.schemas import (
    TransactionCreate, TransactionUpdate, TransactionResponse, TransactionSearchFilter
)
from backend.app.transactions.service import TransactionService
from backend.app.transactions.models import TransactionType

router = APIRouter(prefix="/transactions", tags=["Transaction Management"])

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.create_transaction(db, current_user.id, data)

@router.get("", response_model=List[TransactionResponse])
async def list_transactions(
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    transaction_type: Optional[TransactionType] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    is_recurring: Optional[bool] = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    filters = TransactionSearchFilter(
        account_id=account_id,
        category_id=category_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        search=search,
        min_amount=min_amount,
        max_amount=max_amount,
        is_recurring=is_recurring,
        limit=limit,
        offset=offset
    )
    items, total = await TransactionService.list_transactions(db, current_user.id, filters)
    return items

@router.get("/{tx_id}", response_model=TransactionResponse)
async def get_transaction(
    tx_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.get_transaction(db, current_user.id, tx_id)

@router.put("/{tx_id}", response_model=TransactionResponse)
async def update_transaction(
    tx_id: int,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionService.update_transaction(db, current_user.id, tx_id, data)

@router.delete("/{tx_id}")
async def delete_transaction(
    tx_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await TransactionService.delete_transaction(db, current_user.id, tx_id)
    return {"message": "Transaction deleted successfully"}
