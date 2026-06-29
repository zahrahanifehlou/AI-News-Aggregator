# app/services/pipeline.py

from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.services.classifier import Classifier
from app.agents.news_agent import NewsRankingAgent
from app.config import RSS_FEEDS
from app.models.article import Article

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
        articles=articles[1:2]
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
    processed.sort(key=lambda x: x.score, reverse=True)

    return processed