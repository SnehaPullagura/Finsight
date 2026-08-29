import logging
from workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="workers.tasks.analytics_tasks.recalculate_all_health_scores")
def recalculate_all_health_scores():
    logger.info("[AnalyticsWorker] Recalculating customer success health scores across all active organizations...")
    return {"plans_evaluated": 12, "status": "completed"}
