# app/workers/tasks.py
from app.workers.celery_app import celery
from app.core.database import SessionLocal
from app.repositories.article_repository import ArticleRepository
from app.services.pipeline.orchestrator import NewsPipeline
from app.services.newsletter import NewsletterBuilder
from app.services.email_sender import EmailSender

@celery.task(bind=True)
def run_pipeline_task(self):
    db = SessionLocal()
    try:
        repo = ArticleRepository()
        pipeline = NewsPipeline(repo)

        inserted_articles = pipeline.run(db)

        if not inserted_articles:
            print("No new articles today")
            return {"inserted": 0}

        html = NewsletterBuilder().build_html(inserted_articles)

        EmailSender().send(
            to_email="hanifelo@live.com",
            subject="Daily AI News Digest",
            html_content=html
        )
        return {"inserted": len(inserted_articles)}
    except Exception as exc:
        print(f"Task failed: {exc}")
        # Optional: retry
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()