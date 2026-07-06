# app/workers/celery_app.py

from celery import Celery
from app.config import BROKER_URL, RESULT_BACKEND

celery = Celery(
    "news_worker",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)