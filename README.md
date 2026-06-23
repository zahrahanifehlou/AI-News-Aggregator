# AI News Aggregator

A Python-based news aggregator that collects content from multiple sources, stores it in PostgreSQL, generates summaries, and emails a daily digest.

## Features

- **Multi-source collection**: RSS/Atom feeds, YouTube channels, OpenAI blog, Fox News, and any custom RSS source.
- **Scheduled workers**: Uses APScheduler to collect content and send digests on a cadence you configure.
- **PostgreSQL storage**: SQLAlchemy models with duplicate detection.
- **AI summarization**: OpenAI-powered summaries with a fallback extractive summarizer.
- **Email digest**: HTML digest sent via SMTP at a configured time each day.
- **Dockerized**: Ready to run with `docker compose up`.

## Project Structure

```
.
├── app/
│   ├── collectors/          # Source-specific collectors
│   │   ├── base.py          # Base collector interface
│   │   ├── rss_collector.py # Generic RSS/Atom collector
│   │   ├── youtube_collector.py
│   │   ├── openai_blog_collector.py
│   │   └── fox_news_collector.py
│   ├── config.py            # Pydantic settings from env vars
│   ├── database.py          # SQLAlchemy engine & sessions
│   ├── models.py            # Article model
│   ├── summarizer.py        # Summary generation
│   ├── emailer.py           # SMTP digest sender
│   ├── scheduler.py         # APScheduler jobs
│   └── main.py              # CLI entry point
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

1. **Copy the environment file and configure it**:

   ```bash
   cp .env.example .env
   # Edit .env with your SMTP credentials, OpenAI API key, and timezone
   ```

2. **Run with Docker Compose**:

   ```bash
   docker compose up --build
   ```

   This starts PostgreSQL and the aggregator scheduler. Collectors run every `COLLECTION_INTERVAL_MINUTES` and the digest is sent at the configured time.

## Local Development (without Docker)

1. **Install dependencies**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL** and create the `ainews` database.

3. **Configure `.env`** (see `.env.example`).

4. **Run the scheduler**:

   ```bash
   python -m app.main run
   ```

5. **Run collectors once**:

   ```bash
   python -m app.main collect
   ```

6. **Send a digest once**:

   ```bash
   python -m app.main digest
   ```

## Adding Sources

### RSS feed

Add any RSS collector by passing a name and feed URL:

```python
from app.collectors.rss_collector import RssCollector

collector = RssCollector("techcrunch", "https://techcrunch.com/feed/")
collector.collect()
```

### YouTube channel

YouTube channels are collected via public RSS feeds (no API key required). You need the channel ID:

```python
from app.collectors.youtube_collector import YouTubeCollector

collector = YouTubeCollector(
    channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
    channel_name="Google Developers"
)
collector.collect()
```

To register collectors permanently, add them to `app/scheduler.py` in `run_all_collectors`.

## Configuration

All settings are loaded from environment variables (`.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/ainews` |
| `COLLECTION_INTERVAL_MINUTES` | How often to collect content | `60` |
| `SUMMARY_SEND_HOUR` | Hour of the daily digest (24h) | `8` |
| `SUMMARY_SEND_MINUTE` | Minute of the daily digest | `0` |
| `TIMEZONE` | Timezone for scheduler | `UTC` |
| `OPENAI_API_KEY` | OpenAI API key for summaries | `None` |
| `OPENAI_MODEL` | Model name | `gpt-4o-mini` |
| `SUMMARY_MAX_LENGTH` | Target summary length in words | `250` |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_FROM` / `SMTP_TO` | SMTP settings | Gmail defaults |
| `SMTP_TLS` | Use STARTTLS | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DAYS_TO_KEEP` | Days to retain articles | `30` |

## Notes

- YouTube collection uses public channel RSS feeds, so it does not need a YouTube API key.
- Fox News uses the official Fox News RSS feed.
- OpenAI blog scraping uses a lightweight HTML parser.
- If `OPENAI_API_KEY` is not set, the fallback summarizer returns the first few sentences of the article.
