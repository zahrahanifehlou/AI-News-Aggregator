# app/workers/celery_app.py
from celery import Celery
from celery.schedules import crontab

from app.config import BROKER_URL, RESULT_BACKEND


celery = Celery(
    "news_worker",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

# ------------------------
# Config
# ------------------------
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    enable_utc=False,
)

# ------------------------
# Schedule tasks
# ------------------------
celery.conf.beat_schedule = {
    'run-daily-news-pipeline': {
        'task': 'app.workers.tasks.run_pipeline_task',
        'schedule': crontab(hour=20, minute=0),
    },
}