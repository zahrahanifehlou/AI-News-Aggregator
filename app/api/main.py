"""FastAPI application exposing the AI news pipeline and digest endpoints."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from app.models.article import Article
from app.services.pipeline import process_news, send_newsletter

logger = logging.getLogger(__name__)


class ArticleResponse(BaseModel):
    title: str
    score: float
    categories: list[str]
    summary: str
    url: str
    source: str
    published_at: str

    @classmethod
    def from_article(cls, article: Article) -> "ArticleResponse":
        return cls(
            title=article.title,
            score=article.score,
            categories=article.categories or [],
            summary=article.summary,
            url=article.url,
            source=article.source,
            published_at=article.published_at,
        )


class NewsletterResponse(BaseModel):
    count: int
    articles: list[ArticleResponse]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.latest_news = []
    yield


app = FastAPI(
    title="AI News Pipeline API",
    description="Daily AI News collection, ranking & newsletter service",
    version="1.1.0",
    lifespan=lifespan,
)


def _serialize(articles: list[Article]) -> list[ArticleResponse]:
    return [ArticleResponse.from_article(a) for a in articles]


@app.get("/")
async def home() -> dict[str, str]:
    return {"status": "ok", "service": "AI News Digest API"}


@app.post("/run-pipeline")
async def run_pipeline() -> dict[str, object]:
    """Trigger the full news collection + ranking pipeline."""
    try:
        news = await run_in_threadpool(process_news)
    except Exception:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail="Pipeline failed")

    app.state.latest_news = news
    return {"message": "Pipeline completed successfully", "article_count": len(news)}


@app.post("/send-newsletter", response_model=NewsletterResponse)
async def send_newsletter_endpoint(background_tasks: BackgroundTasks) -> NewsletterResponse:
    """Send a newsletter with the current latest news."""
    if not app.state.latest_news:
        raise HTTPException(status_code=400, detail="No news available. Run pipeline first.")

    background_tasks.add_task(send_newsletter, app.state.latest_news)
    return NewsletterResponse(
        count=len(app.state.latest_news),
        articles=_serialize(app.state.latest_news),
    )


@app.get("/news", response_model=list[ArticleResponse])
async def get_news(
    limit: int = Query(50, ge=1, le=200, description="Number of articles to return"),
) -> list[ArticleResponse]:
    """Return current news (sorted by score)."""
    return _serialize(app.state.latest_news[:limit])


@app.get("/news/top", response_model=list[ArticleResponse])
async def get_top_news(
    limit: int = Query(5, ge=1, le=20),
) -> list[ArticleResponse]:
    """Return the top N articles."""
    return _serialize(app.state.latest_news[:limit])


@app.get("/news/category/{category}", response_model=list[ArticleResponse])
async def get_by_category(
    category: str,
    limit: int = Query(50, ge=1, le=100),
) -> list[ArticleResponse]:
    """Filter news by category (case-insensitive)."""
    target = category.lower()
    filtered = [
        a
        for a in app.state.latest_news
        if target in [c.lower() for c in (a.categories or [])]
    ]
    return _serialize(filtered[:limit])


@app.get("/health")
async def health() -> dict[str, object]:
    return {"status": "healthy", "news_count": len(app.state.latest_news)}
