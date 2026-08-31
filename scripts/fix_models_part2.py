import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/proposal.py
    write_file("backend/app/models/proposal.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Proposal(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "proposals"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    proposal_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    terms_and_conditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    custom_sections: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    line_items: Mapped[List["ProposalLineItem"]] = relationship("ProposalLineItem", back_populates="proposal", cascade="all, delete-orphan")

class ProposalLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "proposal_line_items"

    proposal_id: Mapped[str] = mapped_column(String(36), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    proposal: Mapped["Proposal"] = relationship("Proposal", back_populates="line_items")
""")

    # 2. models/quote.py
    write_file("backend/app/models/quote.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Quote(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "quotes"

    quote_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    line_items: Mapped[List["QuoteLineItem"]] = relationship("QuoteLineItem", back_populates="quote", cascade="all, delete-orphan")

class QuoteLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "quote_line_items"

    quote_id: Mapped[str] = mapped_column(String(36), ForeignKey("quotes.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    discount_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    quote: Mapped["Quote"] = relationship("Quote", back_populates="line_items")
""")

    # 3. models/invoice.py
    write_file("backend/app/models/invoice.py", """import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class Invoice(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    deal_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("deals.id", ondelete="SET NULL"), nullable=True, index=True)
    quote_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("quotes.id", ondelete="SET NULL"), nullable=True)
    company_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    contact_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    payment_status: Mapped[str] = mapped_column(String(50), default="unpaid", nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    subtotal: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    line_items: Mapped[List["InvoiceLineItem"]] = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    payments: Mapped[List["InvoicePayment"]] = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLineItem(UUIDModel, TimestampMixin):
    __tablename__ = "invoice_line_items"

    invoice_id: Mapped[str] = mapped_column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)
    tax_rate_pct: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="line_items")

class InvoicePayment(UUIDModel, TimestampMixin):
    __tablename__ = "invoice_payments"

    invoice_id: Mapped[str] = mapped_column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), default="bank_transfer", nullable=False)
    transaction_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="payments")
""")

    # 4. models/campaign.py
    write_file("backend/app/models/campaign.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CampaignSegment(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "campaign_segments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_entity: Mapped[str] = mapped_column(String(50), default="contact", nullable=False)
    filter_criteria: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    campaigns: Mapped[List["Campaign"]] = relationship("Campaign", back_populates="segment")

class Campaign(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), default="email", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False, index=True)
    segment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("campaign_segments.id", ondelete="SET NULL"), nullable=True)
    template_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_recipients: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    open_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    click_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversion_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    budget: Mapped[Optional[float]] = mapped_column(Numeric(18, 2), nullable=True)
    revenue_attributed: Mapped[float] = mapped_column(Numeric(18, 2), default=0.0, nullable=False)

    segment: Mapped[Optional["CampaignSegment"]] = relationship("CampaignSegment", back_populates="campaigns")
    recipients: Mapped[List["CampaignRecipient"]] = relationship("CampaignRecipient", back_populates="campaign", cascade="all, delete-orphan")

class CampaignRecipient(UUIDModel, TimestampMixin):
    __tablename__ = "campaign_recipients"

    campaign_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="recipients")
""")

    # 5. models/automation.py
    write_file("backend/app/models/automation.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class AutomationWorkflow(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "automation_workflows"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    trigger_event: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    trigger_config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    conditions: Mapped[List["WorkflowCondition"]] = relationship("WorkflowCondition", back_populates="workflow", cascade="all, delete-orphan")
    actions: Mapped[List["WorkflowAction"]] = relationship("WorkflowAction", back_populates="workflow", cascade="all, delete-orphan", order_by="WorkflowAction.execution_order.asc()")
    execution_logs: Mapped[List["WorkflowExecutionLog"]] = relationship("WorkflowExecutionLog", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowCondition(UUIDModel):
    __tablename__ = "workflow_conditions"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    field_path: Mapped[str] = mapped_column(String(100), nullable=False)
    operator: Mapped[str] = mapped_column(String(20), nullable=False)
    target_value: Mapped[str] = mapped_column(String(255), nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="conditions")

class WorkflowAction(UUIDModel):
    __tablename__ = "workflow_actions"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    action_config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    execution_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="actions")

class WorkflowExecutionLog(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "workflow_execution_logs"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payload_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="execution_logs")
""")

    # 6. models/custom_field.py & models/audit.py
    write_file("backend/app/models/custom_field.py", """import uuid
from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.models.base import Base, UUIDModel, TimestampMixin, TenantMixin

class CustomFieldDefinition(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "custom_field_definitions"

    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    field_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    field_type: Mapped[str] = mapped_column(String(50), nullable=False)
    options_list: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
""")

    write_file("backend/app/models/audit.py", """import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TenantMixin

class AuditLog(UUIDModel, TenantMixin):
    __tablename__ = "audit_logs"

    actor_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    actor_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    before_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    after_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

    actor: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
""")

    print("Part 2 models normalized.")

if __name__ == '__main__':
    run()
