
from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from app.services.pipeline import process_news, send_newsletter
from app.models.article import Article
class ArticleResponse(BaseModel):
    title: str
    score: float
    categories: List[str]
    summary: str
    url: str
    source: str
    published_at: str


class NewsletterResponse(BaseModel):
    count: int
    articles: List[ArticleResponse]

app = FastAPI(
    title="AI News Pipeline API",
    description="Daily AI News collection, ranking & newsletter service",
    version="1.1.0"
)

@app.on_event("startup")
async def startup_event():
    app.state.latest_news: List[Article] = []



@app.get("/")
async def home():
    return {"status": "ok", "service": "AI News Digest API"}


@app.post("/run-pipeline")
async def run_pipeline(background_tasks: BackgroundTasks):
    """Trigger the full news collection + ranking pipeline."""
    try:
        # Run in background if you expect this to take > few seconds
        news = process_news()
        app.state.latest_news = news
        return {
            "message": "Pipeline completed successfully",
            "article_count": len(news)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@app.post("/send-newsletter", response_model=NewsletterResponse)
async def send_newsletter_endpoint(background_tasks: BackgroundTasks):
    """Send newsletter with current latest news."""
    if not app.state.latest_news:
        raise HTTPException(status_code=400, detail="No news available. Run pipeline first.")

    try:
        # Fire-and-forget email sending in background
        background_tasks.add_task(send_newsletter, app.state.latest_news)
        
        return {
            "count": len(app.state.latest_news),
            "articles": [
                ArticleResponse(
                    title=a.title,
                    score=a.score,
                    categories=a.categories or [],
                    summary=a.summary,
                    url=a.url,
                    source=a.source,
                    published_at=a.published_at
                )
                for a in app.state.latest_news
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send newsletter: {str(e)}")


@app.get("/news", response_model=List[ArticleResponse])
async def get_news(
    limit: Optional[int] = Query(50, ge=1, le=200, description="Number of articles to return")
):
    """Return all current news (sorted by score)."""
    return [
        ArticleResponse(
            title=a.title,
            score=a.score,
            categories=a.categories or [],
            summary=a.summary,
            url=a.url,
            source=a.source,
            published_at=a.published_at
        )
        for a in app.state.latest_news[:limit]
    ]


@app.get("/news/top", response_model=List[ArticleResponse])
async def get_top_news(
    limit: Optional[int] = Query(5, ge=1, le=20)
):
    """Return top N articles."""
    top = app.state.latest_news[:limit]
    return [
        ArticleResponse(
            title=a.title,
            score=a.score,
            categories=a.categories or [],
            summary=a.summary,
            url=a.url,
            source=a.source,
            published_at=a.published_at
        )
        for a in top
    ]


@app.get("/news/category/{category}", response_model=List[ArticleResponse])
async def get_by_category(
    category: str,
    limit: Optional[int] = Query(50, ge=1, le=100)
):
    """Filter news by category (case-insensitive)."""
    filtered = [
        a for a in app.state.latest_news
        if category.lower() in [c.lower() for c in (a.categories or [])]
    ]
    return [
        ArticleResponse(
            title=a.title,
            score=a.score,
            categories=a.categories or [],
            summary=a.summary,
            url=a.url,
            source=a.source,
            published_at=a.published_at
        )
        for a in filtered[:limit]
    ]


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "news_count": len(app.state.latest_news)
    }