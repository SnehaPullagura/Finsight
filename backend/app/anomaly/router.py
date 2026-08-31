from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.anomaly.schemas import AnomalyResponse, AnomalyAcknowledgeRequest
from backend.app.anomaly.service import AnomalyDetectionEngine

router = APIRouter(prefix="/anomalies", tags=["Anomaly Detection"])

@router.get("", response_model=List[AnomalyResponse])
async def list_anomalies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AnomalyDetectionEngine.scan_for_anomalies(db, current_user.id)

@router.post("/{anomaly_id}/acknowledge", response_model=AnomalyResponse)
async def acknowledge_anomaly(
    anomaly_id: int,
    data: AnomalyAcknowledgeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await AnomalyDetectionEngine.acknowledge_anomaly(
        db, current_user.id, anomaly_id, data.is_false_positive
    )
