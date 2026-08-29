import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
RESULT_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

celery_app = Celery(
    "clientflow_workers",
    broker=REDIS_URL,
    backend=RESULT_URL,
    include=[
        "workers.tasks.automation_tasks",
        "workers.tasks.email_tasks",
        "workers.tasks.search_indexer_tasks",
        "workers.tasks.analytics_tasks",
        "workers.tasks.ai_tasks",
        "workers.tasks.maintenance_tasks"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1,
)

# Scheduled Periodic Beat Jobs
celery_app.conf.beat_schedule = {
    "monitor-support-sla-breaches": {
        "task": "workers.tasks.maintenance_tasks.check_sla_violations",
        "schedule": crontab(minute="*/15"),
    },
    "recalculate-customer-health-scores": {
        "task": "workers.tasks.analytics_tasks.recalculate_all_health_scores",
        "schedule": crontab(minute="0", hour="*/2"),
    },
    "execute-scheduled-campaigns": {
        "task": "workers.tasks.email_tasks.process_scheduled_campaigns",
        "schedule": crontab(minute="*/5"),
    },
    "cleanup-expired-sessions": {
        "task": "workers.tasks.maintenance_tasks.cleanup_expired_tokens",
        "schedule": crontab(hour="3", minute="0"),
    }
}
