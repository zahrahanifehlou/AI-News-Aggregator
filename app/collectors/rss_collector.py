"""Generic RSS/Atom feed collector."""

import logging
from datetime import datetime
from typing import Generator

import feedparser
import requests

from app.collectors.base import BaseCollector, ContentItem
from app.models import ContentType

logger = logging.getLogger(__name__)


def _parse_published(entry) -> datetime | None:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])
    return None


def _fetch_feed(url: str, timeout: int = 30) -> feedparser.FeedParserDict:
    """Fetch and parse an RSS/Atom feed with a user-agent."""
    response = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return feedparser.parse(response.content)


class RssCollector(BaseCollector):
    """Collect articles from an RSS or Atom feed URL."""

    def __init__(self, name: str, feed_url: str):
        super().__init__(name)
        self.feed_url = feed_url

    def fetch(self) -> Generator[ContentItem, None, None]:
        logger.info("Collecting RSS feed: %s", self.feed_url)
        try:
            feed = _fetch_feed(self.feed_url)
        except Exception as exc:
            logger.error("Failed to fetch RSS feed %s: %s", self.feed_url, exc)
            return

        for entry in feed.entries:
            external_id = entry.get("id") or entry.get("link") or entry.get("title")
            yield ContentItem(
                external_id=external_id,
                title=entry.get("title", "Untitled"),
                url=entry.get("link", ""),
                content_type=ContentType.ARTICLE,
                published_at=_parse_published(entry),
                summary=entry.get("summary") or entry.get("description"),
                content=entry.get("content", [{}])[0].get("value") if entry.get("content") else None,
                author=entry.get("author"),
                image_url=None,
            )
