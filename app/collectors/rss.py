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

            # Better content extraction
            content = self._extract_content(entry)

            published = getattr(entry, "published", "") or getattr(entry, "pubDate", "")

            article = Article(
                title=title,
                content=content,
                url=url,
                published_at=published,
                source=self.source_name,
            )

            articles.append(article)
   

        return articles

    def _extract_content(self, entry):
        """Try multiple possible fields for content"""
        # Priority order
        if hasattr(entry, "content") and entry.content:
            # content is usually a list of dicts
            return entry.content[0].get('value', "")

        # Most common fields
        content = getattr(entry, "description", "") or getattr(entry, "summary", "")
        
        # Fallback: try encoded content (some feeds use this)
        if not content:
            content = getattr(entry, "content:encoded", "") or getattr(entry, "content_encoded", "")

        return content.strip()