from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.search import GlobalSearchResponse
from backend.app.services.search import GlobalSearchService

router = APIRouter()

@router.get("", response_model=GlobalSearchResponse)
async def global_search(
    q: str = Query(..., min_length=1, description="Global search query across CRM"),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = GlobalSearchService(db)
    return await service.search(q, tenant_id=tenant_id)
