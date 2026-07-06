# app/api/routes/pipeline.py

from fastapi import APIRouter
from app.workers.tasks import run_pipeline_task

router = APIRouter()

@router.post("/run-pipeline")
def run_pipeline():
    task = run_pipeline_task.delay()
    return {"task_id": task.id}




## without celery
# @router.post("/run-pipeline")
# def run_pipeline():
#     from app.core.database import SessionLocal
#     from app.repositories.article_repository import ArticleRepository
#     from app.services.pipeline.orchestrator import NewsPipeline
    
#     db = SessionLocal()
#     try:
#         repo = ArticleRepository()
#         pipeline = NewsPipeline(repo)
#         inserted = pipeline.run(db)
#         return {"inserted": inserted}
#     finally:
#         db.close()

# @router.post("/send-newsletter")
# def send_newsletter():
#     from app.services.newsletter import NewsletterBuilder
#     from app.services.email_sender import EmailSender
#     from app.repositories.article_repository import ArticleRepository
#     from app.core.database import SessionLocal
    
#     db = SessionLocal()
#     try:
#         repo = ArticleRepository()
#         articles = repo.get_top(db, limit=20)
        
#         html = NewsletterBuilder().build_html(articles)
        
#         EmailSender().send(
#             to_email="hanifelo@live.com",
#             subject="Daily AI News Digest",
#             html_content=html
#         )
        
#         return {"sent": len(articles)}
#     finally:
#         db.close()
#         db.close()