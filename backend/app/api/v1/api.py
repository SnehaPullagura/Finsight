from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals
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
