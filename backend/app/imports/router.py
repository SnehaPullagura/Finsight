from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.imports.schemas import ImportJobResponse
from backend.app.imports.service import DataImportPipeline

router = APIRouter(prefix="/imports", tags=["Data Import Pipeline"])

@router.post("/upload", response_model=ImportJobResponse, status_code=status.HTTP_201_CREATED)
async def upload_bank_statement(
    account_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    return await DataImportPipeline.process_file_content(
        db, current_user.id, account_id, file.filename, content
    )
