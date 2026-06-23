"""Base collector interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Generator

from app.database import db_session
from app.models import Article, ContentType


@dataclass
class ContentItem:
    """Normalized content item produced by any collector."""

    external_id: str
    title: str
    url: str
    content_type: ContentType
    published_at: datetime | None
    summary: str | None = None
    content: str | None = None
    author: str | None = None
    image_url: str | None = None


class BaseCollector(ABC):
    """Base class for all content collectors."""

    source_name: str
    content_type: ContentType = ContentType.ARTICLE

    def __init__(self, name: str | None = None):
        self.source_name = name or self.__class__.__name__

    @abstractmethod
    def fetch(self) -> Generator[ContentItem, None, None]:
        """Yield normalized content items from the source."""
        raise NotImplementedError

    def _store(self, items: list[ContentItem]) -> int:
        """Persist a list of content items, skipping duplicates."""
        inserted = 0
        with db_session() as session:
            for item in items:
                exists = (
                    session.query(Article)
                    .filter_by(external_id=item.external_id, source=self.source_name)
                    .first()
                )
                if exists:
                    continue

                article = Article(
                    external_id=item.external_id,
                    source=self.source_name,
                    content_type=item.content_type,
                    title=item.title,
                    url=item.url,
                    summary=item.summary,
                    content=item.content,
                    author=item.author,
                    published_at=item.published_at,
                    image_url=item.image_url,
                )
                session.add(article)
                inserted += 1
        return inserted

    def collect(self) -> int:
        """Fetch and store all items from this source."""
        items = list(self.fetch())
        return self._store(items)
