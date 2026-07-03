from celery import Celery
from app.config import broker, backend

celery = Celery(
    "news_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# IMPORTANT: force task discovery
celery.conf.imports = [
    "app.services.tasks",
]

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)