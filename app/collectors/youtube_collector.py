"""YouTube channel collector using YouTube's public RSS feeds."""

import logging
from datetime import datetime
from typing import Generator

import feedparser
import requests

from app.collectors.base import BaseCollector, ContentItem
from app.models import ContentType

logger = logging.getLogger(__name__)

YOUTUBE_CHANNEL_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def _parse_published(entry) -> datetime | None:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    return None


class YouTubeCollector(BaseCollector):
    """Collect recent videos from a YouTube channel via public RSS."""

    content_type = ContentType.VIDEO

    def __init__(self, channel_id: str, channel_name: str | None = None):
        name = channel_name or f"youtube-{channel_id}"
        super().__init__(name)
        self.channel_id = channel_id
        self.feed_url = YOUTUBE_CHANNEL_RSS.format(channel_id=channel_id)

    def fetch(self) -> Generator[ContentItem, None, None]:
        logger.info("Collecting YouTube channel: %s", self.channel_id)
        try:
            response = requests.get(
                self.feed_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                },
                timeout=30,
            )
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except Exception as exc:
            logger.error("Failed to fetch YouTube channel %s: %s", self.channel_id, exc)
            return

        for entry in feed.entries:
            yield ContentItem(
                external_id=entry.get("yt_videoid") or entry.get("id"),
                title=entry.get("title", "Untitled"),
                url=entry.get("link", ""),
                content_type=ContentType.VIDEO,
                published_at=_parse_published(entry),
                summary=entry.get("summary") or entry.get("media_description"),
                content=None,
                author=entry.get("author"),
                image_url=None,
            )
