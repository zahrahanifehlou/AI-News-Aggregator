from sqlalchemy import text

def insert_articles(engine, articles):
    query = text("""
        INSERT INTO articles (title, summary, url, published_at, source , score, score_breakdown , categories)
        VALUES (:title, :summary, :url, :published_at, :source, :score, :score_breakdown, :categories)
    """)

    with engine.begin() as conn:  # auto commit
        for article in articles:
            conn.execute(query, {
                "title": article.title,
                "summary": article.summary,
                "url": article.url,
                "published_at": article.published_at,
                "source": article.source,
                "score": article.score,
                "score_breakdown": list(article.score_breakdown),
                "categories": article.categories,
            })