from typing import List
from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException, Query
from app.services.tasks import process_news, send_newsletter_task
from app.workers.celery_worker import celery
from app.models.article import ArticleResponse

app = FastAPI(
    title="AI News Pipeline API",
    description="Daily AI News collection, ranking & newsletter service",
    version="2.0.0",
)

@app.get("/")
def home():
    return {
        "status": "ok",
        "service": "AI News Digest API",
    }


# ---------------------------------------------------
# Run Pipeline
# ---------------------------------------------------

@app.post("/run-pipeline")
def run_pipeline():
    ## with fastAPI
    from app.services.pipeline import run_news_pipeline
    run_news_pipeline()
    return {"message": "Pipeline executed successfully"}
    
    ## with celery
    # task = process_news.delay()
    # return {
    #     "message": "Pipeline queued successfully",
    #     "task_id": task.id,
    #     "status": task.status,
    # }


# ---------------------------------------------------
# Task Status
# ---------------------------------------------------

# @app.get("/tasks/{task_id}")
# def get_task_status(task_id: str):

#     task = AsyncResult(task_id, app=celery)

#     return {
#         "task_id": task.id,
#         "state": task.state,
#         "result": task.result,
#     }


# ---------------------------------------------------
# Send Newsletter
# ---------------------------------------------------

@app.post("/send-newsletter")
def send_newsletter_endpoint():
    # with FastAPI
    from app.services.pipeline import send_newsletter
    send_newsletter()
    return {"message": "Newsletter sent successfully"}
    
    # with Celery
    # task = send_newsletter_task.delay()
    # return {
    #     "message": "Newsletter queued",
    #     "task_id": task.id,
    #     "status": task.status,
    # }


# ---------------------------------------------------
# Get All News
# ---------------------------------------------------

@app.get("/news", response_model=List[ArticleResponse])
def get_news():
    from app.services.pipeline import get_top_articles
    articles = get_top_articles(limit=20)

    return articles


# ---------------------------------------------------
# Top News
# ---------------------------------------------------

@app.get("/news/top", response_model=List[ArticleResponse])
def get_top_news(
    limit: int = Query(5, ge=1, le=20)
):

    from app.services.pipeline import get_top_articles
    articles = get_top_articles(limit=limit)
    return articles


# ---------------------------------------------------
# Category Filter
# ---------------------------------------------------

@app.get("/news/category/{category}", response_model=List[ArticleResponse])
def get_news_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
):

    from app.database.database import get_news_by_category
    articles = get_news_by_category(category=category, limit=limit)

    return articles


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get("/health")
def health():

    from app.database.database import get_top_articles
    articles = get_top_articles(limit=1)
    count = len(articles)

    return {
        "status": "healthy",
        "article_count": count,
    }