# app/workers/celery_app.py

from celery import Celery
from app.config import broker , backend

celery = Celery(
    "news_worker",
    broker=broker,
    backend=backend,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)