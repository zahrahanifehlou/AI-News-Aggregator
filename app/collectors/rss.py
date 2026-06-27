import feedparser
from app.models.article import Article


class RSSCollector:
    """
    Generic RSS collector that can fetch and normalize RSS feeds.
    """

    def __init__(self, source_name: str, url: str):
        self.source_name = source_name
        self.url = url

    def collect(self):
        feed = feedparser.parse(self.url)

        articles = []

        for entry in feed.entries:
            title = getattr(entry, "title", "No title")
            url = getattr(entry, "link", "")

            published = getattr(entry, "published", "")
            content = getattr(entry, "content", "")

            article = Article(
                title=title,
                content=content,
                url=url,
                published_at=published,
                source=self.source_name,
            )

            articles.append(article)

        return articles