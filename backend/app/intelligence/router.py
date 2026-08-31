from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.intelligence.schemas import CategorizationRequest, CategorizationResponse
from backend.app.intelligence.service import TransactionIntelligenceService

router = APIRouter(prefix="/intelligence", tags=["Transaction Intelligence"])

@router.post("/categorize", response_model=CategorizationResponse)
async def categorize_transaction(
    data: CategorizationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await TransactionIntelligenceService.categorize(db, data.description, data.amount)
