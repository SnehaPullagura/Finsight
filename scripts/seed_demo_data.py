import asyncio
import os
import sys
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.abspath("."))
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///clientflow.db"
os.environ["DATABASE_SYNC_URL"] = "sqlite:///clientflow.db"

from backend.app.models.base import Base
from backend.app.core.database import async_engine, AsyncSessionLocal
from backend.app.core.security import get_password_hash
from backend.app.models.auth import User, Role, Permission, UserRole
from backend.app.models.organization import Organization, OrganizationMember, Team, TeamMember
from backend.app.models.contact import Contact
from backend.app.models.company import Company
from backend.app.models.lead import Lead, LeadScoringRule
from backend.app.models.pipeline import Pipeline, PipelineStage
from backend.app.models.deal import Deal, DealProduct
from backend.app.models.activity import Activity
from backend.app.models.task import Task
from backend.app.models.calendar import CalendarEvent, EventAttendee
from backend.app.models.product import Product, ProductCategory
from backend.app.models.proposal import Proposal, ProposalLineItem
from backend.app.models.quote import Quote, QuoteLineItem
from backend.app.models.invoice import Invoice, InvoiceLineItem, InvoicePayment
from backend.app.models.support import Ticket, TicketComment
from backend.app.models.customer_success import CustomerSuccessPlan, OnboardingMilestone
from backend.app.models.campaign import Campaign, CampaignSegment
from backend.app.models.automation import AutomationWorkflow, WorkflowCondition, WorkflowAction
from backend.app.models.custom_field import CustomFieldDefinition

async def seed():
    print("Initializing SQLite database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        print("Seeding full enterprise demo dataset...")

        tenant_id = "org-apex-001"
        org = Organization(
            id=tenant_id,
            name="Apex Global Dynamics",
            slug="apex-global",
            domain="apexglobal.internal",
            plan_tier="enterprise",
            is_active=True,
            settings={"currency": "USD", "timezone": "UTC"}
        )
        db.add(org)

        admin_user = User(
            id="user-alex-001",
            email="admin@clientflow.internal",
            hashed_password=get_password_hash("AdminSecret123!"),
            first_name="Alexander",
            last_name="Vance",
            is_active=True,
            is_verified=True,
            is_superuser=True
        )
        db.add(admin_user)
        await db.flush()

        member = OrganizationMember(
            organization_id=org.id,
            user_id=admin_user.id,
            is_owner=True,
            status="active"
        )
        db.add(member)

        c1 = Company(
            id="comp-stark-01",
            tenant_id=tenant_id,
            name="Stark Industries",
            domain="starkindustries.internal",
            industry="technology",
            annual_revenue=15000000.0,
            currency="USD",
            employee_count=1200,
            city="New York",
            country="USA"
        )
        c2 = Company(
            id="comp-wayne-02",
            tenant_id=tenant_id,
            name="Wayne Enterprises",
            domain="wayneenterprises.internal",
            industry="finance",
            annual_revenue=28000000.0,
            currency="USD",
            employee_count=3500,
            city="Gotham",
            country="USA"
        )
        db.add_all([c1, c2])
        await db.flush()

        ct1 = Contact(
            id="cont-pepper-01",
            tenant_id=tenant_id,
            company_id=c1.id,
            first_name="Pepper",
            last_name="Potts",
            email="pepper.potts@starkindustries.internal",
            phone="+1-555-0192",
            title="Chief Executive Officer",
            lifecycle_stage="customer",
            lead_source="referral"
        )
        ct2 = Contact(
            id="cont-lucius-02",
            tenant_id=tenant_id,
            company_id=c2.id,
            first_name="Lucius",
            last_name="Fox",
            email="lucius.fox@wayneenterprises.internal",
            phone="+1-555-0843",
            title="Chief Technology Officer",
            lifecycle_stage="opportunity",
            lead_source="inbound_web"
        )
        db.add_all([ct1, ct2])

        lead1 = Lead(
            id="lead-elon-01",
            tenant_id=tenant_id,
            first_name="Tony",
            last_name="Stark",
            email="tony.stark@starkindustries.internal",
            company_name="Stark Industries",
            status="qualified",
            source="inbound_web",
            score=95,
            qualification_grade="A",
            estimated_budget=250000.0,
            employee_count=1200,
            intent_score=98,
            engagement_count=12
        )
        lead2 = Lead(
            id="lead-bruce-02",
            tenant_id=tenant_id,
            first_name="Bruce",
            last_name="Wayne",
            email="bruce@wayneenterprises.internal",
            company_name="Wayne Enterprises",
            status="new",
            source="direct_outreach",
            score=85,
            qualification_grade="A",
            estimated_budget=500000.0,
            employee_count=3500,
            intent_score=90,
            engagement_count=4
        )
        db.add_all([lead1, lead2])

        pipe = Pipeline(
            id="pipe-standard-01",
            tenant_id=tenant_id,
            name="Enterprise Direct Sales",
            is_default=True,
            is_active=True
        )
        db.add(pipe)
        await db.flush()

        st1 = PipelineStage(id="stg-discovery-01", tenant_id=tenant_id, pipeline_id=pipe.id, name="Discovery & Scoping", stage_order=1, probability=20, stage_type="open", sla_days=14)
        st2 = PipelineStage(id="stg-proposal-02", tenant_id=tenant_id, pipeline_id=pipe.id, name="Proposal & Review", stage_order=2, probability=50, stage_type="open", sla_days=21)
        st3 = PipelineStage(id="stg-negotiation-03", tenant_id=tenant_id, pipeline_id=pipe.id, name="Contract Negotiation", stage_order=3, probability=80, stage_type="open", sla_days=10)
        st4 = PipelineStage(id="stg-won-04", tenant_id=tenant_id, pipeline_id=pipe.id, name="Closed Won", stage_order=4, probability=100, stage_type="won")
        db.add_all([st1, st2, st3, st4])
        await db.flush()

        d1 = Deal(
            id="deal-arc-01",
            tenant_id=tenant_id,
            name="Enterprise Arc Fusion Platform",
            value=250000.0,
            currency="USD",
            probability=80,
            pipeline_id=pipe.id,
            stage_id=st3.id,
            company_id=c1.id,
            contact_id=ct1.id,
            owner_id=admin_user.id,
            status="open"
        )
        d2 = Deal(
            id="deal-surveillance-02",
            tenant_id=tenant_id,
            name="Advanced AI Security Operations",
            value=450000.0,
            currency="USD",
            probability=50,
            pipeline_id=pipe.id,
            stage_id=st2.id,
            company_id=c2.id,
            contact_id=ct2.id,
            owner_id=admin_user.id,
            status="open"
        )
        db.add_all([d1, d2])

        p1 = Product(
            id="prod-core-01",
            tenant_id=tenant_id,
            name="ClientFlow Enterprise Cloud",
            sku="CF-ENT-001",
            unit_price=120000.0,
            currency="USD",
            tax_rate_pct=5.0,
            is_active=True,
            is_service=True
        )
        db.add(p1)
        await db.flush()

        prop1 = Proposal(
            id="prop-001",
            tenant_id=tenant_id,
            title="Enterprise Cloud Migration & Platform License",
            proposal_number="PROP-2026-001",
            deal_id=d1.id,
            company_id=c1.id,
            contact_id=ct1.id,
            status="accepted",
            subtotal=240000.0,
            discount_amount=20000.0,
            tax_amount=11000.0,
            total_amount=231000.0,
            currency="USD"
        )
        db.add(prop1)

        inv1 = Invoice(
            id="inv-001",
            tenant_id=tenant_id,
            invoice_number="INV-2026-001",
            deal_id=d1.id,
            company_id=c1.id,
            contact_id=ct1.id,
            status="issued",
            payment_status="paid",
            issue_date=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=20),
            subtotal=231000.0,
            tax_amount=0.0,
            total_amount=231000.0,
            amount_paid=231000.0,
            currency="USD"
        )
        db.add(inv1)

        cs1 = CustomerSuccessPlan(
            id="cs-stark-01",
            tenant_id=tenant_id,
            company_id=c1.id,
            owner_id=admin_user.id,
            status="active",
            health_score=94,
            health_grade="good",
            target_renewal_date=date.today() + timedelta(days=330),
            renewal_value=250000.0,
            goals=["Complete SOC2 SSO integration", "Onboard 250 sales reps", "Deploy AI copilot workflows"]
        )
        db.add(cs1)

        t1 = Ticket(
            id="tkt-001",
            tenant_id=tenant_id,
            ticket_number="TCK-1001",
            subject="Assistance with SAML Okta SSO Configuration",
            description="Configuring tenant identity provider metadata for enterprise single sign-on.",
            priority="medium",
            status="resolved",
            category="technical",
            company_id=c1.id,
            contact_id=ct1.id,
            resolved_at=datetime.utcnow()
        )
        db.add(t1)

        act1 = Activity(
            id="act-001",
            tenant_id=tenant_id,
            entity_type="deal",
            entity_id=d1.id,
            activity_type="CALL",
            title="Executive Alignment Call with Pepper Potts",
            description="Finalized contract terms and signed off on proposal.",
            performed_at=datetime.utcnow() - timedelta(hours=2),
            metadata_json={}
        )
        db.add(act1)

        task1 = Task(
            id="tsk-001",
            tenant_id=tenant_id,
            title="Conduct Q3 Architecture Review",
            description="Review API rate limits and OpenSearch cluster health.",
            priority="high",
            status="pending",
            due_date=datetime.utcnow() + timedelta(days=2),
            is_recurring=False
        )
        db.add(task1)

        await db.commit()
        print("SUCCESS: Database initialized and seeded with full enterprise records!")

if __name__ == '__main__':
    asyncio.run(seed())
