from app.workers.celery_worker import celery
from app.services.pipeline import run_news_pipeline
from app.services.pipeline import send_newsletter


@celery.task(name="app.services.tasks.process_news")
def process_news():
    return run_news_pipeline()


@celery.task(name="app.services.tasks.send_newsletter_task")
def send_newsletter_task():
    return send_newsletter()