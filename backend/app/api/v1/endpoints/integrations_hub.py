from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_tenant_id
from backend.app.integrations.schemas import (
    ConnectionCreateRequest,
    ConnectionResponse,
    MigrationPreviewRequest,
    MigrationPreviewResponse
)
from backend.app.integrations.models import IntegrationConnection
from backend.app.integrations.migration_engine import DataMigrationEngine

router = APIRouter()

@router.post("/connections", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def create_connection(
    req: ConnectionCreateRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    conn = IntegrationConnection(
        tenant_id=tenant_id,
        provider=req.provider,
        name=req.name,
        auth_type=req.auth_type,
        credentials_encrypted=req.credentials,
        settings=req.settings or {},
        status="connected",
        is_active=True
    )
    db.add(conn)
    await db.flush()
    await db.refresh(conn)
    return conn

@router.post("/migrate-preview", response_model=MigrationPreviewResponse)
async def preview_data_migration(req: MigrationPreviewRequest):
    rows = DataMigrationEngine.parse_csv_to_dicts(req.csv_content)
    valid, rejected = DataMigrationEngine.map_and_transform_contacts(rows, req.field_mappings)

    return MigrationPreviewResponse(
        total_parsed=len(rows),
        valid_count=len(valid),
        rejected_count=len(rejected),
        sample_valid=valid[:5],
        sample_rejected=rejected[:5]
    )
