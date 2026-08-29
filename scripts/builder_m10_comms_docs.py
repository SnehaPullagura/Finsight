import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. models/communication.py & models/document.py
    write_file("backend/app/models/communication.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class CommunicationMessage(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "communication_messages"

    channel: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # email, sms, internal_message, webhook
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    subject: Optional[Mapped[str]] = mapped_column(String(500), nullable=True)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    body_html: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[str] = mapped_column(String(50), default="sent", nullable=False, index=True) # draft, queued, sent, delivered, opened, failed
    tracking_id: Optional[Mapped[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    
    # Associated CRM entity
    entity_type: Optional[Mapped[str]] = mapped_column(String(50), nullable=True, index=True)
    entity_id: Optional[Mapped[str]] = mapped_column(String(36), nullable=True, index=True)
    
    user_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    sent_at: Optional[Mapped[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    user: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")

class CommunicationTemplate(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "communication_templates"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="email", nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="general", nullable=False) # sales, support, marketing, onboarding
    
    subject_template: Optional[Mapped[str]] = mapped_column(String(500), nullable=True)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    available_variables: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
""")

    write_file("backend/app/models/document.py", """import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class DocumentFolder(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "document_folders"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("document_folders.id", ondelete="CASCADE"), nullable=True)

    documents: Mapped[List["Document"]] = relationship("Document", back_populates="folder", cascade="all, delete-orphan")

class Document(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "documents"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    sha256_hash: Optional[Mapped[str]] = mapped_column(String(64), nullable=True)
    
    folder_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("document_folders.id", ondelete="SET NULL"), nullable=True)
    
    # Associated CRM entity
    entity_type: Optional[Mapped[str]] = mapped_column(String(50), nullable=True, index=True)
    entity_id: Optional[Mapped[str]] = mapped_column(String(36), nullable=True, index=True)
    
    uploaded_by_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)

    folder: Mapped[Optional["DocumentFolder"]] = relationship("DocumentFolder", back_populates="documents")
    uploaded_by: Mapped[Optional["backend.app.models.auth.User"]] = relationship("backend.app.models.auth.User")
    versions: Mapped[List["DocumentVersion"]] = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")

class DocumentVersion(UUIDModel, TimestampMixin):
    __tablename__ = "document_versions"

    document_id: Mapped[str] = mapped_column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    sha256_hash: Optional[Mapped[str]] = mapped_column(String(64), nullable=True)
    uploaded_by_id: Optional[Mapped[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    document: Mapped["Document"] = relationship("Document", back_populates="versions")
""")

    # 2. Schemas
    write_file("backend/app/schemas/communication.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

class SendMessageRequest(BaseModel):
    channel: str = Field("email", description="email, sms, internal_message")
    recipient: str
    subject: Optional[str] = None
    body_text: str
    body_html: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    template_id: Optional[str] = None
    template_vars: Optional[Dict[str, Any]] = None

class CommunicationMessageResponse(BaseModel):
    id: str
    tenant_id: str
    channel: str
    sender: str
    recipient: str
    subject: Optional[str] = None
    body_text: str
    body_html: Optional[str] = None
    status: str
    tracking_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class CommunicationTemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    channel: Optional[str] = "email"
    category: Optional[str] = "general"
    subject_template: Optional[str] = None
    body_template: str
    available_variables: Optional[List[str]] = None

class CommunicationTemplateResponse(BaseModel):
    id: str
    name: str
    channel: str
    category: str
    subject_template: Optional[str] = None
    body_template: str
    available_variables: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True
""")

    write_file("backend/app/schemas/document.py", """from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DocumentFolderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_id: Optional[str] = None

class DocumentFolderResponse(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    file_size_bytes: int
    mime_type: str
    folder_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    uploaded_by_id: Optional[str] = None
    is_public: bool
    download_count: int
    tags: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True
""")

    # 3. Repositories
    write_file("backend/app/repositories/communication.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.communication import CommunicationMessage, CommunicationTemplate
from backend.app.repositories.base import BaseRepository

class CommunicationRepository(BaseRepository[CommunicationMessage]):
    def __init__(self, db: AsyncSession):
        super().__init__(CommunicationMessage, db)

    async def list_for_entity(self, entity_type: str, entity_id: str, tenant_id: str) -> List[CommunicationMessage]:
        query = select(CommunicationMessage).where(
            CommunicationMessage.tenant_id == tenant_id,
            CommunicationMessage.entity_type == entity_type,
            CommunicationMessage.entity_id == entity_id,
            CommunicationMessage.is_deleted == False
        ).order_by(CommunicationMessage.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

class TemplateRepository(BaseRepository[CommunicationTemplate]):
    def __init__(self, db: AsyncSession):
        super().__init__(CommunicationTemplate, db)
""")

    write_file("backend/app/repositories/document.py", """from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.document import Document, DocumentFolder
from backend.app.repositories.base import BaseRepository

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db: AsyncSession):
        super().__init__(Document, db)

    async def list_for_entity(self, entity_type: str, entity_id: str, tenant_id: str) -> List[Document]:
        query = select(Document).where(
            Document.tenant_id == tenant_id,
            Document.entity_type == entity_type,
            Document.entity_id == entity_id,
            Document.is_deleted == False
        ).order_by(Document.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

class DocumentFolderRepository(BaseRepository[DocumentFolder]):
    def __init__(self, db: AsyncSession):
        super().__init__(DocumentFolder, db)
""")

    # 4. Services
    write_file("backend/app/services/communication.py", """import uuid
from datetime import datetime
from jinja2 import Template
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.communication import CommunicationMessage, CommunicationTemplate
from backend.app.repositories.communication import CommunicationRepository, TemplateRepository
from backend.app.services.base import BaseService
from backend.app.schemas.communication import SendMessageRequest, CommunicationTemplateCreate
from backend.app.core.config import settings

class CommunicationService(BaseService[CommunicationMessage, CommunicationRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(CommunicationRepository(db))
        self.template_repo = TemplateRepository(db)

    async def send_message(self, req: SendMessageRequest, tenant_id: str, sender_email: str, user_id: Optional[str] = None) -> CommunicationMessage:
        subject = req.subject
        body_text = req.body_text
        body_html = req.body_html

        # If template is specified, render with Jinja2
        if req.template_id:
            tpl = await self.template_repo.get_by_id(req.template_id, tenant_id=tenant_id)
            if tpl:
                template_context = req.template_vars or {}
                if tpl.subject_template:
                    subject = Template(tpl.subject_template).render(**template_context)
                body_text = Template(tpl.body_template).render(**template_context)
                body_html = f"<div style='font-family:sans-serif;'>{body_text.replace(chr(10), '<br/>')}</div>"

        tracking_id = str(uuid.uuid4())
        msg = await self.repository.create({
            "channel": req.channel,
            "sender": sender_email or settings.EMAILS_FROM_EMAIL,
            "recipient": req.recipient,
            "subject": subject,
            "body_text": body_text,
            "body_html": body_html,
            "status": "sent",
            "tracking_id": tracking_id,
            "entity_type": req.entity_type,
            "entity_id": req.entity_id,
            "user_id": user_id,
            "sent_at": datetime.utcnow(),
            "metadata_json": {}
        }, tenant_id=tenant_id)

        # Log an activity entry on the entity timeline
        if req.entity_type and req.entity_id:
            from backend.app.models.activity import Activity
            activity = Activity(
                tenant_id=tenant_id,
                entity_type=req.entity_type,
                entity_id=req.entity_id,
                activity_type="EMAIL" if req.channel == "email" else "NOTE",
                title=f"Sent {req.channel.upper()}: {subject or 'Message'}",
                description=body_text[:500],
                performed_at=datetime.utcnow(),
                user_id=user_id
            )
            self.repository.db.add(activity)
            await self.repository.db.flush()

        return msg
""")

    write_file("backend/app/services/document.py", """import os
import hashlib
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.config import settings
from backend.app.models.document import Document, DocumentFolder, DocumentVersion
from backend.app.repositories.document import DocumentRepository, DocumentFolderRepository
from backend.app.services.base import BaseService

class DocumentService(BaseService[Document, DocumentRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(DocumentRepository(db))
        self.folder_repo = DocumentFolderRepository(db)

    async def save_uploaded_file(
        self,
        filename: str,
        content: bytes,
        mime_type: str,
        tenant_id: str,
        uploaded_by_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Document:
        upload_dir = os.path.join(settings.STORAGE_LOCAL_ROOT, tenant_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        sha256 = hashlib.sha256(content).hexdigest()
        stored_filename = f"{sha256[:16]}_{filename}"
        file_path = os.path.join(upload_dir, stored_filename)
        
        with open(file_path, "wb") as f:
            f.write(content)

        doc = await self.repository.create({
            "name": filename,
            "file_path": file_path,
            "file_size_bytes": len(content),
            "mime_type": mime_type,
            "sha256_hash": sha256,
            "folder_id": folder_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "uploaded_by_id": uploaded_by_id,
            "is_public": False,
            "download_count": 0,
            "tags": tags or []
        }, tenant_id=tenant_id)

        # Initial version
        ver = DocumentVersion(
            document_id=doc.id,
            version_number=1,
            file_path=file_path,
            file_size_bytes=len(content),
            sha256_hash=sha256,
            uploaded_by_id=uploaded_by_id
        )
        self.repository.db.add(ver)
        await self.repository.db.flush()

        return doc
""")

    # 5. Endpoints
    write_file("backend/app/api/v1/endpoints/communications.py", """from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_user, get_current_tenant_id, CurrentUserContext
from backend.app.schemas.communication import (
    SendMessageRequest,
    CommunicationMessageResponse,
    CommunicationTemplateCreate,
    CommunicationTemplateResponse
)
from backend.app.services.communication import CommunicationService

router = APIRouter()

@router.post("/send", response_model=CommunicationMessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    req: SendMessageRequest,
    current_user: CurrentUserContext = Depends(get_current_user),
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    return await service.send_message(req, tenant_id=tenant_id, sender_email=current_user.email, user_id=current_user.id)

@router.get("/history/{entity_type}/{entity_id}", response_model=List[CommunicationMessageResponse])
async def get_history(
    entity_type: str,
    entity_id: str,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    return await service.repository.list_for_entity(entity_type, entity_id, tenant_id)

@router.post("/templates", response_model=CommunicationTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    req: CommunicationTemplateCreate,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    data = req.model_dump(exclude_unset=True)
    if "available_variables" not in data or data["available_variables"] is None:
        data["available_variables"] = []
    return await service.template_repo.create(data, tenant_id=tenant_id)

@router.get("/templates", response_model=List[CommunicationTemplateResponse])
async def list_templates(
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    service = CommunicationService(db)
    return await service.template_repo.list(tenant_id=tenant_id)
""")

    write_file("backend/app/api/v1/endpoints/documents.py", """from fastapi import APIRouter, Depends, File, Form, UploadFile, status
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
""")

    # 6. Update api/v1/api.py
    write_file("backend/app/api/v1/api.py", """from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health, auth, organizations, contacts, companies, leads, pipelines, deals,
    activities, tasks, calendar, communications, documents
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
""")

    print("Milestones 12 & 13 Comms and Docs created successfully!")

if __name__ == '__main__':
    run()
