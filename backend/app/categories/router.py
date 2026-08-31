from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.categories.schemas import CategoryResponse
from backend.app.categories.service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories & Taxonomy"])

@router.get("", response_model=List[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryService.list_categories(db)
