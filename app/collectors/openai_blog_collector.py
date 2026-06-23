"""OpenAI blog collector."""

import logging
from datetime import datetime
from typing import Generator
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.collectors.base import BaseCollector, ContentItem
from app.models import ContentType

logger = logging.getLogger(__name__)

OPENAI_BLOG_URL = "https://openai.com/news/"


def _parse_date_text(text: str) -> datetime | None:
    """Try common date formats found on the OpenAI blog."""
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None


class OpenAIBlogCollector(BaseCollector):
    """Collect articles from the OpenAI news/blog index."""

    def __init__(self):
        super().__init__("openai-blog")

    def fetch(self) -> Generator[ContentItem, None, None]:
        logger.info("Collecting OpenAI blog from %s", OPENAI_BLOG_URL)
        try:
            response = requests.get(
                OPENAI_BLOG_URL,
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
        except Exception as exc:
            logger.error("Failed to fetch OpenAI blog: %s", exc)
            return

        soup = BeautifulSoup(response.text, "lxml")
        seen = set()
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href in ("/news", "/news/"):
                continue
            if not href.startswith("/news/") or "?" in href:
                continue
            if href in seen:
                continue
            seen.add(href)

            url = urljoin(OPENAI_BLOG_URL, href)
            title_tag = link.find(["h2", "h3", "h4", "span", "p"])
            title = title_tag.get_text(strip=True) if title_tag else link.get_text(strip=True)
            if not title:
                continue
            external_id = href.rstrip("/").split("/")[-1]
            yield ContentItem(
                external_id=external_id,
                title=title,
                url=url,
                content_type=ContentType.ARTICLE,
                published_at=None,
                summary=None,
                content=None,
                author="OpenAI",
                image_url=None,
            )
