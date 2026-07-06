# app/api/routes/news.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.article_repository import ArticleRepository

router = APIRouter()

repo = ArticleRepository()


@router.get("/news")
def get_news(db: Session = Depends(get_db)):
    return repo.get_top(db, limit=20)


@router.get("/news/top")
def get_top_news(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    return repo.get_top(db, limit=limit)


@router.get("/news/category/{category}")
def get_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return repo.get_by_category(db, category, limit)