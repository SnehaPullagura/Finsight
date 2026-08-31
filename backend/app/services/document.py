import os
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
