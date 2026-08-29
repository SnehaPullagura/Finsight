import uuid
from datetime import datetime
from jinja2 import Template
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.communication import CommunicationMessage, CommunicationTemplate
from backend.app.repositories.communication import CommunicationRepository, TemplateRepository
from backend.app.services.base import BaseService
from backend.app.schemas.communication import SendMessageRequest, CommunicationTemplateCreate
from backend.app.core.config import settings

class CommunicationService(BaseService[CommunicationMessage, CommunicationRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CommunicationRepository(db))
        self.template_repo = TemplateRepository(db)

    async def send_message(self, req: SendMessageRequest, tenant_id: str, sender_email: str, user_id: Optional[str] = None) -> CommunicationMessage:
        subject = req.subject
        body_text = req.body_text
        body_html = req.body_html

        # If template is specified, render with Jinja2
        if req.template_id:
            tpl = await self.template_repo.get_by_id(req.template_id, tenant_id=tenant_id)
            if tpl:
                template_context = req.template_vars or {}
                if tpl.subject_template:
                    subject = Template(tpl.subject_template).render(**template_context)
                body_text = Template(tpl.body_template).render(**template_context)
                body_html = f"<div style='font-family:sans-serif;'>{body_text.replace(chr(10), '<br/>')}</div>"

        tracking_id = str(uuid.uuid4())
        msg = await self.repository.create({
            "channel": req.channel,
            "sender": sender_email or settings.EMAILS_FROM_EMAIL,
            "recipient": req.recipient,
            "subject": subject,
            "body_text": body_text,
            "body_html": body_html,
            "status": "sent",
            "tracking_id": tracking_id,
            "entity_type": req.entity_type,
            "entity_id": req.entity_id,
            "user_id": user_id,
            "sent_at": datetime.utcnow(),
            "metadata_json": {}
        }, tenant_id=tenant_id)

        # Log an activity entry on the entity timeline
        if req.entity_type and req.entity_id:
            from backend.app.models.activity import Activity
            activity = Activity(
                tenant_id=tenant_id,
                entity_type=req.entity_type,
                entity_id=req.entity_id,
                activity_type="EMAIL" if req.channel == "email" else "NOTE",
                title=f"Sent {req.channel.upper()}: {subject or 'Message'}",
                description=body_text[:500],
                performed_at=datetime.utcnow(),
                user_id=user_id
            )
            self.repository.db.add(activity)
            await self.repository.db.flush()

        return msg
