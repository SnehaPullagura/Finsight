from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals,
    activities, tasks, calendar, communications, documents,
    products, proposals, quotes, invoices, support, customer_success,
    campaigns, automations, search, analytics, cpq, billing, advanced_analytics,
    integrations_hub, dag_workflows, governance
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Authorization"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations & Teams"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads & Qualification"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["Sales Pipelines"])
api_router.include_router(deals.router, prefix="/deals", tags=["Deals"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activity Timeline"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(communications.router, prefix="/communications", tags=["Communication System"])
api_router.include_router(documents.router, prefix="/documents", tags=["Document Management"])
api_router.include_router(products.router, prefix="/products", tags=["Product Catalog"])
api_router.include_router(proposals.router, prefix="/proposals", tags=["Proposals"])
api_router.include_router(quotes.router, prefix="/quotes", tags=["Quotes"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
api_router.include_router(support.router, prefix="/support", tags=["Customer Support"])
api_router.include_router(customer_success.router, prefix="/customer-success", tags=["Customer Success"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Marketing Campaigns"])
api_router.include_router(automations.router, prefix="/automations", tags=["Workflow Automation"])
api_router.include_router(search.router, prefix="/search", tags=["Global Search"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & Dashboard"])
api_router.include_router(cpq.router, prefix="/cpq", tags=["CPQ & Pricing Engine"])
api_router.include_router(billing.router, prefix="/billing", tags=["Subscription Billing"])
api_router.include_router(advanced_analytics.router, prefix="/advanced-analytics", tags=["Advanced Analytics & Forecasting"])
api_router.include_router(integrations_hub.router, prefix="/integrations-hub", tags=["Integrations Hub & Migration"])
api_router.include_router(dag_workflows.router, prefix="/dag-workflows", tags=["DAG Workflow Engine"])
api_router.include_router(governance.router, prefix="/governance", tags=["Data Governance & Compliance"])
