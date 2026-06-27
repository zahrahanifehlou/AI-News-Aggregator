from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.config import RSS_FEEDS

summarizer = Summarizer()
deduplicator = Deduplicator()

all_articles = []

for source, url in RSS_FEEDS.items():

    collector = RSSCollector(source, url)

    articles = collector.collect()

    for article in articles:
        article = summarizer.summarize(article)
        all_articles.append(article)

unique_articles = deduplicator.remove_duplicates(all_articles)

print(f"Collected: {len(all_articles)}")
print(f"Unique: {len(unique_articles)}")

for article in unique_articles:
    print(article.title)
    # # insert articles into database
    # from app.database.database import insert_articles
    # from app.config import DATABASE_URL
    # from sqlalchemy import create_engine

    # engine = create_engine(DATABASE_URL)
    # insert_articles(engine, all_articles)
    # print(f"Inserted {len(all_articles)} articles into the database---Phase 2 Complete")


if __name__ == "__main__":
    run()