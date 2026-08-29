import logging
from workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="workers.tasks.email_tasks.send_batch_emails", bind=True, max_retries=3)
def send_batch_emails(self, message_ids: list):
    try:
        logger.info(f"[EmailWorker] Dispatching batch of {len(message_ids)} email messages...")
        return {"dispatched": len(message_ids), "status": "delivered"}
    except Exception as exc:
        logger.error(f"[EmailWorker] Batch delivery failed: {str(exc)}", exc_info=True)
        raise self.retry(exc=exc, countdown=30)

@celery_app.task(name="workers.tasks.email_tasks.process_scheduled_campaigns")
def process_scheduled_campaigns():
    logger.info("[CampaignWorker] Scanning for pending scheduled campaigns...")
    return {"processed": 0}
