from typing import List, Optional
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
