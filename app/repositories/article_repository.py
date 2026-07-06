# app/repositories/article_repository.py

from sqlalchemy import text
import json

class ArticleRepository:

    def insert_many(self, db, articles):
        if not articles:
            return 0

        query = text("""
            INSERT INTO articles (
                title, content, url, published_at,
                source, summary, score_breakdown, categories
            )
            VALUES (
                :title, :content, :url, :published_at,
                :source, :summary, :score_breakdown, :categories
            )
        """)

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
        print("inserted articles:", len(payload))
        return len(payload)

    def get_top(self, db, limit: int = 20):
        result = db.execute(text("""
            SELECT title, content, url, published_at, source,
                   score_breakdown, categories
            FROM articles
            ORDER BY published_at DESC
            LIMIT :limit
        """), {"limit": limit})

        return result.mappings().all()

    def get_by_category(self, db, category: str, limit: int = 20):
        result = db.execute(text("""
            SELECT title, content, url, published_at, source,
                score_breakdown, categories
            FROM articles
            WHERE EXISTS (
                SELECT 1 
                FROM jsonb_array_elements_text(categories) AS cat 
                WHERE cat ILIKE :category
            )
            ORDER BY published_at DESC
            LIMIT :limit
        """), {
            "category": f"%{category}%", 
            "limit": limit
        })

        return result.mappings().all()