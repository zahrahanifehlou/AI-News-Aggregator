from sqlalchemy import text

def insert_articles(engine, articles):
    query = text("""
        INSERT INTO articles (title, summary, url, published_at, source)
        VALUES (:title, :summary, :url, :published_at, :source)
    """)

    with engine.begin() as conn:  # auto commit
        for article in articles:
            conn.execute(query, {
                "title": article.title,
                "summary": article.summary,
                "url": article.url,
                "published_at": article.published_at,
                "source": article.source,
            })