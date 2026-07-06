from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import json
from sqlalchemy import text
from app.config import DATABASE_URL

# ---------------------------------------------------
# Engine (singleton — IMPORTANT for Celery workers)
# ---------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ---------------------------------------------------
# Dependency (FastAPI)
# ---------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------
# Batch insert (optimized + transactional)
# ---------------------------------------------------
def insert_articles(articles):
    """
    Inserts processed articles into DB safely.
    Designed for pipeline/Celery use.
    """

    if not articles:
        return 0

    query = text("""
        INSERT INTO articles (
            title,
            content,
            url,
            published_at,
            source,
            summary,
            score_breakdown,
            categories
        )
        VALUES (
            :title,
            :content,
            :url,
            :published_at,
            :source,
            :summary,
            :score_breakdown,
            :categories
        )
    """)

    db: Session = SessionLocal()

    try:
        payload = []

        for a in articles:
            payload.append({
                "title": a.title,
                "content": getattr(a, "content", None),
                "url": a.url,
                "published_at": a.published_at,
                "source": a.source,
                "summary": a.summary,
                "score_breakdown": json.dumps(getattr(a, "score_breakdown", None))
                if getattr(a, "score_breakdown", None) else None,
                "categories": json.dumps(getattr(a, "categories", None))
                if getattr(a, "categories", None) else None,
            })

        db.execute(query, payload)
        db.commit()
        print("Inserted articles:", len(payload))

        return len(payload)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()







def get_top_articles(limit: int = 20):
    db: Session = SessionLocal()

    try:
        result = db.execute(text("""
            SELECT title, content, url, published_at, source, score_breakdown, categories 
            FROM articles
            ORDER BY published_at DESC
            LIMIT :limit
        """), {"limit": limit})
        rows = result.mappings().all()
        return rows

    finally:
        db.close()
    

def get_news_by_category(category: str, limit: int = 20):
    db: Session = SessionLocal()

    try:
        result = db.execute(text("""
            SELECT title, content, url, published_at, source, score_breakdown, categories
            FROM articles
            WHERE categories LIKE :category
            ORDER BY published_at DESC
            LIMIT :limit
        """), {"category": f"%{category}%", "limit": limit})
        rows = result.mappings().all()
        return rows

    finally:
        db.close()
