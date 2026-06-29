from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.services.classifier import Classifier
from app.agents.news_agent import NewsRankingAgent
from app.config import RSS_FEEDS
from app.services.newsletter import NewsletterBuilder
from app.services.email_sender import EmailSender



def process_news():
    summarizer = Summarizer()
    deduplicator = Deduplicator()
    classifier = Classifier()
    ranker = NewsRankingAgent()
    all_articles = []

    for source, url in RSS_FEEDS.items():
        collector = RSSCollector(source, url)
        articles = collector.collect()
        
        # kepp 5 
        articles = articles[1:5]

        for article in articles:
            article = summarizer.summarize(article)
            all_articles.append(article)

    unique_articles = deduplicator.remove_duplicates(all_articles)

    processed = []

    for article in unique_articles:
        article = classifier.classify(article)
        article = ranker.rank(article)
        processed.append(article)

    final_feed = sorted(processed, key=lambda x: x.score, reverse=True)
    return final_feed   # 🔥 IMPORTANT

def send_newsletter(final_feed):
    builder = NewsletterBuilder()
    sender = EmailSender()
    
    html = builder.build_html(final_feed)

    sender.send(
        to_email="hanifelo@live.com",
        subject="Daily AI News Digest",
        html_content=html
    )

    