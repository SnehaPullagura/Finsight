from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.notifications.schemas import NotificationResponse
from backend.app.notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notification Engine"])

@router.get("", response_model=List[NotificationResponse])
async def list_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await NotificationService.list_notifications(db, current_user.id)

@router.patch("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await NotificationService.mark_as_read(db, current_user.id, notification_id)
    return {"message": "Notification marked as read"}

@router.post("/read-all")
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await NotificationService.mark_all_as_read(db, current_user.id)
    return {"message": "All notifications marked as read"}
