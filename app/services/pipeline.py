"""End-to-end news pipeline: collect, summarize, dedupe, classify, rank and email."""

from __future__ import annotations

import logging

from app.agents.news_agent import NewsRankingAgent
from app.collectors.rss import RSSCollector
from app.config import MAX_ARTICLES_PER_FEED, NEWSLETTER_RECIPIENT, RSS_FEEDS
from app.models.article import Article
from app.services.classifier import Classifier
from app.services.deduplicator import Deduplicator
from app.services.email_sender import EmailSender
from app.services.newsletter import NewsletterBuilder
from app.services.summarizer import Summarizer

logger = logging.getLogger(__name__)


def process_news() -> list[Article]:
    """Collect, summarize, deduplicate, classify and rank articles.

    Returns the articles sorted by descending score.
    """
    summarizer = Summarizer()
    deduplicator = Deduplicator()
    classifier = Classifier()
    ranker = NewsRankingAgent()

    collected: list[Article] = []
    for source, url in RSS_FEEDS.items():
        articles = RSSCollector(source, url).collect()[:MAX_ARTICLES_PER_FEED]
        logger.info("Collected %d articles from %s", len(articles), source)
        for article in articles:
            collected.append(summarizer.summarize(article))

    unique_articles = deduplicator.remove_duplicates(collected)

    processed: list[Article] = []
    for article in unique_articles:
        article = classifier.classify(article)
        article = ranker.rank(article)
        processed.append(article)

    ranked = sorted(processed, key=lambda a: a.score, reverse=True)
    logger.info("Pipeline produced %d ranked articles", len(ranked))
    return ranked


def send_newsletter(articles: list[Article], to_email: str = NEWSLETTER_RECIPIENT) -> None:
    """Build the digest from ``articles`` and email it to ``to_email``."""
    html = NewsletterBuilder().build_html(articles)
    EmailSender().send(
        to_email=to_email,
        subject="Daily AI News Digest",
        html_content=html,
    )
    logger.info("Newsletter sent to %s with %d articles", to_email, len(articles))
