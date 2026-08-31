from fastapi import APIRouter
from backend.app.workflow.schemas import DSRExportRequest
from backend.app.governance.dsr_engine import DataSubjectRightsEngine

router = APIRouter()

@router.post("/dsr/export")
async def export_gdpr_subject_data(req: DSRExportRequest):
    sample_entities = {
        "contacts": [{"email": req.subject_email, "name": "Subject User"}],
        "activities": [{"type": "EMAIL", "subject": "Quarterly Demo"}]
    }
    return DataSubjectRightsEngine.export_subject_data(req.subject_email, sample_entities)
