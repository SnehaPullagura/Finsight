from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from backend.app.notifications.models import Notification, NotificationType

class NotificationService:
    @staticmethod
    async def create_notification(
        db: AsyncSession, user_id: int, notif_type: NotificationType,
        title: str, message: str, action_url: Optional[str] = None
    ) -> Notification:
        notif = Notification(
            user_id=user_id,
            notification_type=notif_type,
            title=title,
            message=message,
            action_url=action_url,
            is_read=False
        )
        db.add(notif)
        await db.commit()
        await db.refresh(notif)
        return notif

    @staticmethod
    async def list_notifications(db: AsyncSession, user_id: int) -> List[Notification]:
        stmt = select(Notification).where(
            Notification.user_id == user_id
        ).order_by(Notification.created_at.desc()).limit(50)
        res = await db.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def mark_as_read(db: AsyncSession, user_id: int, notification_id: int) -> bool:
        await db.execute(
            update(Notification)
            .where(Notification.id == notification_id, Notification.user_id == user_id)
            .values(is_read=True)
        )
        await db.commit()
        return True

    @staticmethod
    async def mark_all_as_read(db: AsyncSession, user_id: int) -> bool:
        await db.execute(
            update(Notification)
            .where(Notification.user_id == user_id)
            .values(is_read=True)
        )
        await db.commit()
        return True
