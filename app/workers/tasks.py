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

        inserted_articles = pipeline.run(db)  # return inserted items

        html = NewsletterBuilder().build_html(inserted_articles)

        EmailSender().send(
            to_email="hanifelo@live.com",
            subject="Daily AI News Digest",
            html_content=html
        )

        return {"inserted": len(inserted_articles)}
    finally:
        db.close()