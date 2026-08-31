import secrets
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.support import Ticket, TicketComment
from backend.app.repositories.support import TicketRepository
from backend.app.services.base import BaseService
from backend.app.schemas.support import TicketCreate, TicketUpdate, TicketCommentCreate

class SupportService(BaseService[Ticket, TicketRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(TicketRepository(db))

    async def create_ticket(self, req: TicketCreate, tenant_id: str, author_id: Optional[str] = None) -> Ticket:
        t_num = f"TCK-{secrets.token_hex(4).upper()}"
        sla_hours = 4 if req.priority == "urgent" else (8 if req.priority == "high" else 24)
        sla_due = datetime.utcnow() + timedelta(hours=sla_hours)

        data = req.model_dump(exclude_unset=True)
        data["ticket_number"] = t_num
        data["created_by_id"] = author_id
        data["sla_due_at"] = sla_due
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}

        ticket = await self.repository.create(data, tenant_id=tenant_id)

        # Log timeline activity if linked to company/contact
        if ticket.company_id:
            from backend.app.models.activity import Activity
            self.repository.db.add(Activity(
                tenant_id=tenant_id,
                entity_type="company",
                entity_id=ticket.company_id,
                activity_type="TASK",
                title=f"Support Ticket Created: {ticket.ticket_number}",
                description=ticket.subject
            ))
            await self.repository.db.flush()

        return ticket

    async def add_comment(self, ticket_id: str, req: TicketCommentCreate, author_id: Optional[str] = None, tenant_id: str = None) -> TicketComment:
        ticket = await self.get(ticket_id, tenant_id=tenant_id)
        comment = TicketComment(
            ticket_id=ticket.id,
            author_id=author_id,
            body=req.body,
            is_internal=req.is_internal or False
        )
        self.repository.db.add(comment)
        await self.repository.db.flush()
        return comment

    async def resolve_ticket(self, ticket_id: str, notes: str, tenant_id: str) -> Ticket:
        ticket = await self.get(ticket_id, tenant_id=tenant_id)
        return await self.repository.update(ticket, {
            "status": "resolved",
            "resolved_at": datetime.utcnow(),
            "resolution_notes": notes
        })
