from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse
from typing import List, Optional
import os
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.core.exceptions import EntityNotFoundException
from backend.app.schemas.document import DocumentResponse, DocumentFolderCreate, DocumentFolderResponse
from backend.app.services.document import DocumentService

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    entity_type: Optional[str] = Form(None),
    entity_id: Optional[str] = Form(None),
    folder_id: Optional[str] = Form(None),
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    service = DocumentService(db)
    return await service.save_uploaded_file(
        filename=file.filename or "uploaded_file",
        content=content,
        mime_type=file.content_type or "application/octet-stream",
        tenant_id=tenant_id,
        uploaded_by_id=current_user.id,
        entity_type=entity_type,
        entity_id=entity_id,
        folder_id=folder_id
    )

@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DocumentService(db)
    if entity_type and entity_id:
        return await service.repository.list_for_entity(entity_type, entity_id, tenant_id)
    return await service.list(tenant_id=tenant_id)

@router.get("/{id}/download")
async def download_document(
    id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DocumentService(db)
    doc = await service.get(id, tenant_id=tenant_id)
    if not os.path.exists(doc.file_path):
        raise EntityNotFoundException("File on disk", doc.name)

    await service.repository.update(doc, {"download_count": doc.download_count + 1})
    return FileResponse(path=doc.file_path, filename=doc.name, media_type=doc.mime_type)

@router.post("/folders", response_model=DocumentFolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(
    req: DocumentFolderCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DocumentService(db)
    return await service.folder_repo.create(req.model_dump(), tenant_id=tenant_id)

@router.get("/folders", response_model=List[DocumentFolderResponse])
async def list_folders(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = DocumentService(db)
    return await service.folder_repo.list(tenant_id=tenant_id)
