import logging
from workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="workers.tasks.ai_tasks.enrich_lead_profile")
def enrich_lead_profile(lead_id: str, tenant_id: str):
    logger.info(f"[AIWorker] Running background LLM enrichment for Lead {lead_id}...")
    return {"lead_id": lead_id, "enriched": True}
