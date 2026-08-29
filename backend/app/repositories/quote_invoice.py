from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.models.proposal import Proposal, ProposalLineItem
from backend.app.models.quote import Quote, QuoteLineItem
from backend.app.models.invoice import Invoice, InvoiceLineItem, InvoicePayment
from backend.app.repositories.base import BaseRepository

class ProposalRepository(BaseRepository[Proposal]):
    def __init__(self, db: AsyncSession):
        super().__init__(Proposal, db)

    async def get_with_items(self, id: str, tenant_id: str) -> Optional[Proposal]:
        query = select(Proposal).where(
            Proposal.id == id,
            Proposal.tenant_id == tenant_id,
            Proposal.is_deleted == False
        ).options(selectinload(Proposal.line_items))
        result = await self.db.execute(query)
        return result.scalars().first()

class QuoteRepository(BaseRepository[Quote]):
    def __init__(self, db: AsyncSession):
        super().__init__(Quote, db)

    async def get_with_items(self, id: str, tenant_id: str) -> Optional[Quote]:
        query = select(Quote).where(
            Quote.id == id,
            Quote.tenant_id == tenant_id,
            Quote.is_deleted == False
        ).options(selectinload(Quote.line_items))
        result = await self.db.execute(query)
        return result.scalars().first()

class InvoiceRepository(BaseRepository[Invoice]):
    def __init__(self, db: AsyncSession):
        super().__init__(Invoice, db)

    async def get_with_items_and_payments(self, id: str, tenant_id: str) -> Optional[Invoice]:
        query = select(Invoice).where(
            Invoice.id == id,
            Invoice.tenant_id == tenant_id,
            Invoice.is_deleted == False
        ).options(selectinload(Invoice.line_items), selectinload(Invoice.payments))
        result = await self.db.execute(query)
        return result.scalars().first()
