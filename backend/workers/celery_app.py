import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "finsight_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300
)

@celery_app.task(name="tasks.aggregate_analytics")
def aggregate_analytics_task(user_id: int):
    return {"status": "success", "user_id": user_id, "task": "analytics_aggregated"}

@celery_app.task(name="tasks.retrain_models")
def retrain_models_task():
    return {"status": "success", "task": "models_retrained"}
