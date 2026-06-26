from app.config import RSS_FEEDS
from app.collectors.rss import RSSCollector


def run():
    all_articles = []

    # Create one collector per source
    for source_name, url in RSS_FEEDS.items():
        collector = RSSCollector(source_name, url)
        articles = collector.collect()
        all_articles.extend(articles)
    print(f"Collected {len(all_articles)} articles---Phase 1 Complete")
    # # Print normalized output
    # for article in all_articles:
    #     print("\n----------------------------")
    #     print(f"Source: {article.source}")
    #     print(f"Title: {article.title}")
    #     print(f"URL: {article.url}")
    #     print(f"Published: {article.published_at}")

    # insert articles into database
    from app.database.database import insert_articles
    from app.config import DATABASE_URL
    from sqlalchemy import create_engine

    engine = create_engine(DATABASE_URL)
    insert_articles(engine, all_articles)
    print(f"Inserted {len(all_articles)} articles into the database---Phase 2 Complete")


if __name__ == "__main__":
    run()