"""Background scheduler for collection and digest tasks."""

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import func

from app.config import get_settings
from app.database import db_session
from app.models import Article

logger = logging.getLogger(__name__)

settings = get_settings()


def run_all_collectors() -> None:
    """Import and run all configured collectors."""
    from app.collectors.fox_news_collector import FoxNewsCollector
    from app.collectors.openai_blog_collector import OpenAIBlogCollector
    from app.collectors.youtube_collector import YouTubeCollector

    collectors = [
        OpenAIBlogCollector(),
        FoxNewsCollector(),
        # Example YouTube channels; replace with channel IDs you care about.
        # YouTubeCollector(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", channel_name="Google Developers"),
    ]

    total = 0
    for collector in collectors:
        try:
            count = collector.collect()
            total += count
            logger.info("Collector %s added %d new items", collector.source_name, count)
        except Exception as exc:
            logger.error("Collector %s failed: %s", collector.source_name, exc)
    logger.info("Collection run complete: %d new items", total)


def send_digest() -> None:
    from app.emailer import prepare_and_send_digest

    try:
        count = prepare_and_send_digest()
        logger.info("Digest sent with %d articles", count)
    except Exception as exc:
        logger.error("Digest send failed: %s", exc)


def cleanup_old_articles() -> None:
    """Remove articles older than the configured retention window."""
    from datetime import datetime, timedelta, timezone

    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.days_to_keep)
    with db_session() as session:
        deleted = session.query(Article).filter(Article.fetched_at < cutoff).delete(
            synchronize_session=False
        )
        logger.info("Cleaned up %d articles older than %d days", deleted, settings.days_to_keep)


def start_scheduler() -> BackgroundScheduler:
    """Start the APScheduler with collection, digest, and cleanup jobs."""
    scheduler = BackgroundScheduler(timezone=settings.timezone)

    scheduler.add_job(
        run_all_collectors,
        trigger=IntervalTrigger(minutes=settings.collection_interval_minutes),
        id="collect_news",
        name="Collect news from all sources",
        replace_existing=True,
    )

    scheduler.add_job(
        send_digest,
        trigger=CronTrigger(
            hour=settings.summary_send_hour,
            minute=settings.summary_send_minute,
        ),
        id="send_digest",
        name="Send daily AI news digest",
        replace_existing=True,
    )

    scheduler.add_job(
        cleanup_old_articles,
        trigger=CronTrigger(hour=2, minute=0),
        id="cleanup_old_articles",
        name="Remove old articles",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        "Scheduler started. Collection every %d minutes. Digest at %02d:%02d %s",
        settings.collection_interval_minutes,
        settings.summary_send_hour,
        settings.summary_send_minute,
        settings.timezone,
    )
    return scheduler
