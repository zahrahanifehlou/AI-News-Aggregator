from app.config import RSS_FEEDS
from app.collectors.rss import RSSCollector


def run():
    all_articles = []

    # Create one collector per source
    for source_name, url in RSS_FEEDS.items():
        collector = RSSCollector(source_name, url)
        articles = collector.collect()
        all_articles.extend(articles)

    # Print normalized output
    for article in all_articles:
        print("\n----------------------------")
        print(f"Source: {article.source}")
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Published: {article.published_at}")


if __name__ == "__main__":
    run()