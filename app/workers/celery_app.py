from celery import Celery
from celery.schedules import crontab

from app.config import BROKER_URL, RESULT_BACKEND

celery = Celery(
    "news_worker",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=['app.workers.tasks'],   # ← This is the key line
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    enable_utc=False,
)

# Direct beat schedule (simpler and more reliable)
celery.conf.beat_schedule = {
    'daily-news-pipeline': {
        'task': 'app.workers.tasks.run_pipeline_task',
        'schedule': crontab(hour=18, minute=0),
    },
}