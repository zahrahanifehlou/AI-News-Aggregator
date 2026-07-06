# app/workers/celery_app.py

from celery import Celery
from app.core.config import CELERY_BROKER_URL

celery = Celery(
    "news_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)