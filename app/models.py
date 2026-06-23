"""SQLAlchemy models for the news aggregator."""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, Integer, String, Text, func

from app.database import Base


class ContentType(str, PyEnum):
    ARTICLE = "article"
    VIDEO = "video"


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(512), nullable=False, index=True)
    source = Column(String(128), nullable=False, index=True)
    content_type = Column(Enum(ContentType), nullable=False, default=ContentType.ARTICLE)
    title = Column(String(512), nullable=False)
    url = Column(String(1024), nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    author = Column(String(256), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    summary_sent_at = Column(DateTime(timezone=True), nullable=True)
    image_url = Column(String(1024), nullable=True)
    is_sent = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        Index("ix_articles_external_id_source", external_id, source, unique=True),
    )

    def __repr__(self) -> str:
        return f"<Article id={self.id} source={self.source} title={self.title[:50]}>"
