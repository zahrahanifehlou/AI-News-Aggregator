# app/services/pipeline/orchestrator.py

from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.services.classifier import Classifier
from app.agents.news_agent import NewsRankingAgent
from app.config import RSS_FEEDS


class NewsPipeline:

    def __init__(self, repo):
        self.repo = repo
        self.summarizer = Summarizer()
        self.deduplicator = Deduplicator()
        self.classifier = Classifier()
        self.ranker = NewsRankingAgent()

    def run(self, db):
        all_articles = []

        # 1. Collect + summarize
        for source, url in RSS_FEEDS.items():
            collector = RSSCollector(source, url)
            articles = collector.collect()[:20]

            for a in articles:
                all_articles.append(self.summarizer.summarize(a))

        # 2. Deduplicate
        unique = self.deduplicator.remove_duplicates(all_articles)

        # 3. Classify + rank
        processed = []
        for a in unique:
            a = self.classifier.classify(a)
            a = self.ranker.rank(a)
            processed.append(a)

        # 4. Sort
        final_feed = sorted(processed, key=lambda x: x.score, reverse=True)

        # 5. Persist
        return self.repo.insert_many(db, final_feed)