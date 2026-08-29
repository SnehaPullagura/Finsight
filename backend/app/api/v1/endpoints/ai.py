from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.ai import (
    AILeadSummaryResponse,
    AIDealRiskAnalysisResponse,
    AIEmailDraftRequest,
    AIEmailDraftResponse,
    AINLQueryRequest,
    AINLQueryResponse
)
from backend.app.services.ai import AIAssistantService

router = APIRouter()

@router.get("/leads/{lead_id}/summary", response_model=AILeadSummaryResponse)
async def get_lead_summary(
    lead_id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = AIAssistantService(db)
    return await service.summarize_lead(lead_id, tenant_id=tenant_id)

@router.get("/deals/{deal_id}/risk-analysis", response_model=AIDealRiskAnalysisResponse)
async def get_deal_risk_analysis(
    deal_id: str,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = AIAssistantService(db)
    return await service.analyze_deal_risk(deal_id, tenant_id=tenant_id)

@router.post("/draft-email", response_model=AIEmailDraftResponse)
async def generate_email_draft(
    req: AIEmailDraftRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = AIAssistantService(db)
    return await service.draft_email(req)

@router.post("/nl-query", response_model=AINLQueryResponse)
async def parse_natural_language_query(
    req: AINLQueryRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = AIAssistantService(db)
    return await service.process_nl_query(req)
