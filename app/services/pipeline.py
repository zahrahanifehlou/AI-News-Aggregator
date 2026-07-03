
from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.services.classifier import Classifier
from app.agents.news_agent import NewsRankingAgent
from app.config import RSS_FEEDS
from app.services.newsletter import NewsletterBuilder
from app.services.email_sender import EmailSender



from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.services.classifier import Classifier
from app.agents.news_agent import NewsRankingAgent
from app.config import RSS_FEEDS
from app.database.database import insert_articles


def run_news_pipeline():
    summarizer = Summarizer()
    deduplicator = Deduplicator()
    classifier = Classifier()
    ranker = NewsRankingAgent()

    all_articles = []

    # 1. Collect + summarize
    for source, url in RSS_FEEDS.items():
        collector = RSSCollector(source, url)
        articles = collector.collect()

        # keep top 5 (clean slice)
        articles = articles[:5]

        for article in articles:
            article = summarizer.summarize(article)
            all_articles.append(article)

    # 2. Deduplicate
    unique_articles = deduplicator.remove_duplicates(all_articles)

    # 3. Classify + rank
    processed = []

    for article in unique_articles:
        article = classifier.classify(article)
        article = ranker.rank(article)
        processed.append(article)

    # 4. Sort by score
    final_feed = sorted(processed, key=lambda x: x.score, reverse=True)

    # 5. Persist to database (IMPORTANT CHANGE)
    insert_articles(final_feed)

    return len(final_feed)

from app.services.email_sender import EmailSender
from app.services.newsletter import NewsletterBuilder
from app.database.database import SessionLocal
from app.models.article import Article


def send_newsletter():
    db = SessionLocal()

    try:
        articles = (
            db.query(Article)
            .order_by(Article.score.desc())
            .limit(20)
            .all()
        )

        html = NewsletterBuilder().build_html(articles)

        EmailSender().send(
            to_email="hanifelo@live.com",
            subject="Daily AI News Digest",
            html_content=html
        )

        return len(articles)

    finally:
        db.close()