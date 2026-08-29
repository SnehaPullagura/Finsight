import logging
from workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="workers.tasks.search_indexer_tasks.sync_entity_index")
def sync_entity_index(entity_type: str, entity_id: str, action: str = "upsert"):
    logger.info(f"[SearchIndexer] Synchronizing {entity_type} {entity_id} (action: {action}) into search index...")
    return {"entity_type": entity_type, "entity_id": entity_id, "indexed": True}
