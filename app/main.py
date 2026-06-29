from app.collectors.rss import RSSCollector
from app.services.summarizer import Summarizer
from app.services.deduplicator import Deduplicator
from app.services.classifier import Classifier
from app.agents.news_agent import NewsRankingAgent
from app.services.newsletter import NewsletterBuilder
from app.services.email_sender import EmailSender
from app.config import RSS_FEEDS


summarizer = Summarizer()
deduplicator = Deduplicator()
classifier = Classifier()
ranker = NewsRankingAgent()

builder = NewsletterBuilder()
sender = EmailSender()

all_articles = []

# 1. Collect + summarize
for source, url in RSS_FEEDS.items():

    collector = RSSCollector(source, url)
    articles = collector.collect()

    for article in articles[1:20]:
        article = summarizer.summarize(article)
        all_articles.append(article)
        print(f"Summarized article: {article.title}")
print(f"Collected {len(all_articles)} articles")

# 2. Deduplicate
unique_articles = deduplicator.remove_duplicates(all_articles)
print(f"Unique articles: {len(unique_articles)}")
# 3. Classify + rank
processed = []

for article in unique_articles:

    article = classifier.classify(article)
    article = ranker.rank(article)

    processed.append(article)

# 4. Sort
final_feed = sorted(processed, key=lambda x: x.score, reverse=True)

# 5. Build newsletter
html = builder.build_html(final_feed)

# 6. Send email
sender.send(
    to_email="hanifelo@live.com",
    subject="Daily AI News Digest",
    html_content=html
)

print("Newsletter sent successfully.")