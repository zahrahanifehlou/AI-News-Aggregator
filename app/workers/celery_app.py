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
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=15),  # 19:15 Paris time
        send_newsletter_task.s(),
    )