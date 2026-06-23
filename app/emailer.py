"""Email digest sender."""

import logging
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import func

from app.config import get_settings
from app.database import db_session
from app.models import Article, ContentType
from app.summarizer import generate_summary

logger = logging.getLogger(__name__)

settings = get_settings()


def _build_html_digest(articles: list[Article]) -> str:
    lines = [
        "<html><body>",
        "<h1>AI News Daily Digest</h1>",
        f"<p>Generated at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>",
        "<hr>",
    ]

    for article in articles:
        summary = article.summary or "No summary available."
        media_label = "Video" if article.content_type == ContentType.VIDEO else "Article"
        lines.append(f"<h2>{article.title}</h2>")
        lines.append(f"<p><strong>Source:</strong> {article.source} | <strong>Type:</strong> {media_label}</p>")
        if article.published_at:
            lines.append(f"<p><strong>Published:</strong> {article.published_at.strftime('%Y-%m-%d %H:%M')}</p>")
        lines.append(f"<p>{summary}</p>")
        lines.append(f'<p><a href="{article.url}">Read more</a></p>')
        lines.append("<hr>")

    lines.append("</body></html>")
    return "\n".join(lines)


def _send_email(subject: str, html_body: str) -> None:
    if not settings.recipient_emails or not settings.smtp_user or not settings.smtp_password:
        logger.warning("Email not configured; skipping send")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.sender_email
    msg["To"] = ", ".join(settings.recipient_emails)
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_tls:
                server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.sender_email, settings.recipient_emails, msg.as_string())
        logger.info("Digest email sent to %s", settings.recipient_emails)
    except Exception as exc:
        logger.error("Failed to send digest email: %s", exc)
        raise


def prepare_and_send_digest() -> int:
    """Summarize recent unsent articles and email the digest."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=1)
    with db_session() as session:
        articles = (
            session.query(Article)
            .filter(Article.published_at >= cutoff, Article.is_sent.is_(False))
            .order_by(Article.published_at.desc())
            .limit(25)
            .all()
        )

        if not articles:
            logger.info("No recent articles to send in digest")
            return 0

        for article in articles:
            if not article.summary:
                article.summary = generate_summary(article.content or article.title, article.title)
            article.is_sent = True
            article.summary_sent_at = func.now()

        digest_html = _build_html_digest(articles)
        _send_email(f"AI News Digest - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}", digest_html)
        return len(articles)
