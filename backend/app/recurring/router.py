from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.recurring.schemas import (
    RecurringPaymentCreate, RecurringPaymentResponse, RecurringCalendarEvent
)
from backend.app.recurring.service import RecurringService

router = APIRouter(prefix="/recurring", tags=["Recurring Payments"])

@router.post("", response_model=RecurringPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_recurring(
    data: RecurringPaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.create_recurring(db, current_user.id, data)

@router.get("", response_model=List[RecurringPaymentResponse])
async def list_recurring(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.list_recurring(db, current_user.id)

@router.post("/detect", response_model=List[RecurringPaymentResponse])
async def detect_recurring_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.detect_recurring(db, current_user.id)

@router.get("/calendar", response_model=List[RecurringCalendarEvent])
async def get_recurring_calendar(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await RecurringService.get_payment_calendar(db, current_user.id)
