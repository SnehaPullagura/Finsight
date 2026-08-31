import secrets
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import EntityNotFoundException, ValidationException
from backend.app.models.proposal import Proposal, ProposalLineItem
from backend.app.models.quote import Quote, QuoteLineItem
from backend.app.models.invoice import Invoice, InvoiceLineItem, InvoicePayment
from backend.app.repositories.quote_invoice import ProposalRepository, QuoteRepository, InvoiceRepository
from backend.app.schemas.quote_invoice import ProposalCreate, QuoteCreate, InvoiceCreate, PaymentRecordCreate

class ProposalService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProposalRepository(db)

    async def create_proposal(self, req: ProposalCreate, tenant_id: str) -> Proposal:
        subtotal = 0.0
        tax_total = 0.0
        discount_total = 0.0

        for item in req.line_items:
            item_gross = item.quantity * item.unit_price
            item_disc = item_gross * ((item.discount_pct or 0.0) / 100.0)
            item_tax = (item_gross - item_disc) * ((item.tax_rate_pct or 0.0) / 100.0)
            subtotal += item_gross
            discount_total += item_disc
            tax_total += item_tax

        total = (subtotal - discount_total) + tax_total
        prop_num = f"PROP-{secrets.token_hex(4).upper()}"

        proposal = await self.repo.create({
            "title": req.title,
            "proposal_number": prop_num,
            "deal_id": req.deal_id,
            "company_id": req.company_id,
            "contact_id": req.contact_id,
            "status": "draft",
            "subtotal": subtotal,
            "discount_amount": discount_total,
            "tax_amount": tax_total,
            "total_amount": total,
            "valid_until": req.valid_until,
            "terms_and_conditions": req.terms_and_conditions,
            "custom_sections": []
        }, tenant_id=tenant_id)

        for item in req.line_items:
            line_tot = (item.quantity * item.unit_price * (1 - (item.discount_pct or 0.0)/100)) * (1 + (item.tax_rate_pct or 0.0)/100)
            li = ProposalLineItem(
                proposal_id=proposal.id,
                product_id=item.product_id,
                item_name=item.item_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount_pct=item.discount_pct or 0.0,
                tax_rate_pct=item.tax_rate_pct or 0.0,
                line_total=line_tot
            )
            self.db.add(li)
        await self.db.flush()

        return proposal

    async def accept_proposal(self, proposal_id: str, tenant_id: str) -> Proposal:
        proposal = await self.repo.get_by_id(proposal_id, tenant_id=tenant_id)
        if not proposal:
            raise EntityNotFoundException("Proposal", proposal_id)
        return await self.repo.update(proposal, {
            "status": "accepted",
            "accepted_at": datetime.utcnow()
        })

class QuoteService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = QuoteRepository(db)

    async def create_quote(self, req: QuoteCreate, tenant_id: str) -> Quote:
        subtotal = sum(i.quantity * i.unit_price for i in req.line_items)
        discount = sum(i.quantity * i.unit_price * ((i.discount_pct or 0.0)/100.0) for i in req.line_items)
        total = subtotal - discount
        q_num = f"QUO-{secrets.token_hex(4).upper()}"

        quote = await self.repo.create({
            "quote_number": q_num,
            "deal_id": req.deal_id,
            "company_id": req.company_id,
            "contact_id": req.contact_id,
            "status": "draft",
            "subtotal": subtotal,
            "discount_amount": discount,
            "tax_amount": 0.0,
            "total_amount": total,
            "expiration_date": req.expiration_date,
            "notes": req.notes
        }, tenant_id=tenant_id)

        for item in req.line_items:
            tot = item.quantity * item.unit_price * (1 - (item.discount_pct or 0.0)/100)
            li = QuoteLineItem(
                quote_id=quote.id,
                product_id=item.product_id,
                item_name=item.item_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount_pct=item.discount_pct or 0.0,
                total_amount=tot
            )
            self.db.add(li)
        await self.db.flush()

        return quote

class InvoiceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = InvoiceRepository(db)

    async def create_invoice(self, req: InvoiceCreate, tenant_id: str) -> Invoice:
        subtotal = sum(i.quantity * i.unit_price for i in req.line_items)
        tax = sum((i.quantity * i.unit_price) * ((i.tax_rate_pct or 0.0)/100.0) for i in req.line_items)
        total = subtotal + tax
        inv_num = f"INV-{secrets.token_hex(4).upper()}"

        invoice = await self.repo.create({
            "invoice_number": inv_num,
            "deal_id": req.deal_id,
            "quote_id": req.quote_id,
            "company_id": req.company_id,
            "contact_id": req.contact_id,
            "status": "issued",
            "payment_status": "unpaid",
            "issue_date": req.issue_date or date.today(),
            "due_date": req.due_date,
            "subtotal": subtotal,
            "tax_amount": tax,
            "total_amount": total,
            "amount_paid": 0.0,
            "notes": req.notes
        }, tenant_id=tenant_id)

        for item in req.line_items:
            tot = (item.quantity * item.unit_price) * (1 + (item.tax_rate_pct or 0.0)/100)
            li = InvoiceLineItem(
                invoice_id=invoice.id,
                item_name=item.item_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                tax_rate_pct=item.tax_rate_pct or 0.0,
                total_amount=tot
            )
            self.db.add(li)
        await self.db.flush()

        return invoice

    async def record_payment(self, invoice_id: str, req: PaymentRecordCreate, tenant_id: str) -> Invoice:
        invoice = await self.repo.get_by_id(invoice_id, tenant_id=tenant_id)
        if not invoice:
            raise EntityNotFoundException("Invoice", invoice_id)

        payment = InvoicePayment(
            invoice_id=invoice.id,
            amount=req.amount,
            payment_method=req.payment_method or "bank_transfer",
            transaction_reference=req.transaction_reference,
            paid_at=datetime.utcnow()
        )
        self.db.add(payment)
        await self.db.flush()

        new_paid = float(invoice.amount_paid or 0.0) + req.amount
        new_status = "paid" if new_paid >= float(invoice.total_amount) else "partially_paid"
        pay_status = "paid" if new_paid >= float(invoice.total_amount) else "partial"

        return await self.repo.update(invoice, {
            "amount_paid": new_paid,
            "status": new_status,
            "payment_status": pay_status
        })
