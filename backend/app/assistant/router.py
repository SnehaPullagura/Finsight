from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.assistant.schemas import AssistantQueryRequest, AssistantQueryResponse
from backend.app.assistant.service import AIFinancialAssistantService

router = APIRouter(prefix="/assistant", tags=["AI Financial Assistant"])

@router.post("/query", response_model=AssistantQueryResponse)
async def query_assistant(
    data: AssistantQueryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AIFinancialAssistantService.process_query(db, current_user.id, data.query)
