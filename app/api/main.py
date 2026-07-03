from typing import List

from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.article import Article
from app.services.tasks import process_news, send_newsletter_task
from app.workers.celery_worker import celery

app = FastAPI(
    title="AI News Pipeline API",
    description="Daily AI News collection, ranking & newsletter service",
    version="2.0.0",
)


class ArticleResponse(BaseModel):
    title: str
    score: float
    categories: List[str]
    summary: str
    url: str
    source: str
    published_at: str

    class Config:
        from_attributes = True


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

    task = process_news.delay()

    return {
        "message": "Pipeline queued successfully",
        "task_id": task.id,
        "status": task.status,
    }


# ---------------------------------------------------
# Task Status
# ---------------------------------------------------

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):

    task = AsyncResult(task_id, app=celery)

    return {
        "task_id": task.id,
        "state": task.state,
        "result": task.result,
    }


# ---------------------------------------------------
# Send Newsletter
# ---------------------------------------------------

@app.post("/send-newsletter")
def send_newsletter_endpoint():

    task = send_newsletter_task.delay()

    return {
        "message": "Newsletter queued",
        "task_id": task.id,
        "status": task.status,
    }


# ---------------------------------------------------
# Get All News
# ---------------------------------------------------

@app.get("/news", response_model=List[ArticleResponse])
def get_news(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):

    articles = (
        db.query(Article)
        .order_by(Article.score.desc())
        .limit(limit)
        .all()
    )

    return articles


# ---------------------------------------------------
# Top News
# ---------------------------------------------------

@app.get("/news/top", response_model=List[ArticleResponse])
def get_top_news(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):

    articles = (
        db.query(Article)
        .order_by(Article.score.desc())
        .limit(limit)
        .all()
    )

    return articles


# ---------------------------------------------------
# Category Filter
# ---------------------------------------------------

@app.get("/news/category/{category}", response_model=List[ArticleResponse])
def get_news_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):

    articles = (
        db.query(Article)
        .filter(Article.categories.contains([category]))
        .order_by(Article.score.desc())
        .limit(limit)
        .all()
    )

    return articles


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get("/health")
def health(db: Session = Depends(get_db)):

    count = db.query(Article).count()

    return {
        "status": "healthy",
        "article_count": count,
    }