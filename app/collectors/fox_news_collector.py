"""Fox News collector."""

from app.collectors.rss_collector import RssCollector

FOX_NEWS_RSS = "https://feeds.foxnews.com/foxnews/latest"


class FoxNewsCollector(RssCollector):
    """Collect latest articles from Fox News RSS feed."""

    def __init__(self):
        super().__init__("fox-news", FOX_NEWS_RSS)
