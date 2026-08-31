from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.support import Ticket, TicketComment
from backend.app.repositories.base import BaseRepository

class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, db: AsyncSession):
        super().__init__(Ticket, db)

    async def get_with_comments(self, id: str, tenant_id: str) -> Optional[Ticket]:
        query = select(Ticket).where(
            Ticket.id == id,
            Ticket.tenant_id == tenant_id,
            Ticket.is_deleted == False
        ).options(selectinload(Ticket.comments).selectinload(TicketComment.author))
        result = await self.db.execute(query)
        return result.scalars().first()
