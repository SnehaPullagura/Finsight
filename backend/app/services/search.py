from typing import Dict, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.contact import Contact
from backend.app.models.company import Company
from backend.app.models.lead import Lead
from backend.app.models.deal import Deal
from backend.app.models.task import Task
from backend.app.models.support import Ticket
from backend.app.models.document import Document
from backend.app.schemas.search import SearchResultItem, GlobalSearchResponse

class GlobalSearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, query_str: str, tenant_id: str, limit_per_entity: int = 5) -> GlobalSearchResponse:
        pattern = f"%{query_str}%"
        all_results = []
        by_type = {}

        # 1. Contacts
        c_stmt = select(Contact).where(
            Contact.tenant_id == tenant_id,
            Contact.is_deleted == False,
            or_(Contact.first_name.ilike(pattern), Contact.last_name.ilike(pattern), Contact.email.ilike(pattern))
        ).limit(limit_per_entity)
        contacts = (await self.db.execute(c_stmt)).scalars().all()
        by_type["contacts"] = [
            SearchResultItem(
                id=c.id,
                entity_type="contact",
                title=f"{c.first_name} {c.last_name}",
                subtitle=c.email,
                url=f"/contacts/{c.id}",
                metadata={"title": c.title, "phone": c.phone}
            ) for c in contacts
        ]
        all_results.extend(by_type["contacts"])

        # 2. Companies
        comp_stmt = select(Company).where(
            Company.tenant_id == tenant_id,
            Company.is_deleted == False,
            or_(Company.name.ilike(pattern), Company.domain.ilike(pattern), Company.industry.ilike(pattern))
        ).limit(limit_per_entity)
        companies = (await self.db.execute(comp_stmt)).scalars().all()
        by_type["companies"] = [
            SearchResultItem(
                id=co.id,
                entity_type="company",
                title=co.name,
                subtitle=co.industry or co.domain,
                url=f"/companies/{co.id}",
                metadata={"domain": co.domain}
            ) for co in companies
        ]
        all_results.extend(by_type["companies"])

        # 3. Leads
        l_stmt = select(Lead).where(
            Lead.tenant_id == tenant_id,
            Lead.is_deleted == False,
            or_(Lead.first_name.ilike(pattern), Lead.last_name.ilike(pattern), Lead.company_name.ilike(pattern), Lead.email.ilike(pattern))
        ).limit(limit_per_entity)
        leads = (await self.db.execute(l_stmt)).scalars().all()
        by_type["leads"] = [
            SearchResultItem(
                id=l.id,
                entity_type="lead",
                title=f"{l.first_name} {l.last_name} ({l.company_name or 'Independent'})",
                subtitle=f"Score: {l.score} | Grade: {l.qualification_grade}",
                url=f"/leads/{l.id}",
                metadata={"status": l.status}
            ) for l in leads
        ]
        all_results.extend(by_type["leads"])

        # 4. Deals
        d_stmt = select(Deal).where(
            Deal.tenant_id == tenant_id,
            Deal.is_deleted == False,
            Deal.name.ilike(pattern)
        ).limit(limit_per_entity)
        deals = (await self.db.execute(d_stmt)).scalars().all()
        by_type["deals"] = [
            SearchResultItem(
                id=d.id,
                entity_type="deal",
                title=d.name,
                subtitle=f"${float(d.value):,.2f} - {d.status.upper()}",
                url=f"/deals/{d.id}",
                metadata={"value": float(d.value)}
            ) for d in deals
        ]
        all_results.extend(by_type["deals"])

        # 5. Tickets
        t_stmt = select(Ticket).where(
            Ticket.tenant_id == tenant_id,
            Ticket.is_deleted == False,
            or_(Ticket.ticket_number.ilike(pattern), Ticket.subject.ilike(pattern))
        ).limit(limit_per_entity)
        tickets = (await self.db.execute(t_stmt)).scalars().all()
        by_type["tickets"] = [
            SearchResultItem(
                id=t.id,
                entity_type="ticket",
                title=f"[{t.ticket_number}] {t.subject}",
                subtitle=f"Status: {t.status} | Priority: {t.priority}",
                url=f"/support/{t.id}",
                metadata={"status": t.status}
            ) for t in tickets
        ]
        all_results.extend(by_type["tickets"])

        return GlobalSearchResponse(
            query=query_str,
            total_results=len(all_results),
            results_by_type=by_type,
            results=all_results
        )
