# app/workers/tasks.py

from app.workers.celery_app import celery
from app.core.database import SessionLocal
from app.repositories.article_repository import ArticleRepository
from app.services.pipeline.orchestrator import NewsPipeline

@celery.task
def run_pipeline_task():
    db = SessionLocal()
    try:
        repo = ArticleRepository()
        pipeline = NewsPipeline(repo)
        inserted = pipeline.run(db)
        return {"inserted": inserted}
    finally:
        db.close()


@celery.task
def send_newsletter_task():
    from app.services.newsletter import NewsletterBuilder
    from app.services.email_sender import EmailSender
    from app.repositories.article_repository import ArticleRepository
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        repo = ArticleRepository()
        articles = repo.get_top(db, limit=20)

        html = NewsletterBuilder().build_html(articles)

        EmailSender().send(
            to_email="hanifelo@live.com",
            subject="Daily AI News Digest",
            html_content=html
        )

        return {"sent": len(articles)}
    finally:
        db.close()