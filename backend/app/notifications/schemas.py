import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.notifications.models import NotificationType

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    notification_type: NotificationType
    title: str
    message: str
    is_read: bool
    action_url: Optional[str] = None
    created_at: datetime.datetime
