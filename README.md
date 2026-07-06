# AI News Aggregator

An automated AI news collection, summarization, ranking, and newsletter delivery pipeline powered by local LLMs via [Ollama](https://ollama.com/).

## Overview

Fetches articles from RSS feeds, summarizes and deduplicates them using semantic embeddings, classifies them into AI-relevant categories, scores them with an LLM-based ranking agent, and delivers a curated HTML newsletter via email — all exposed through a FastAPI REST API with async Celery workers.

## Architecture

```
RSS Feeds
   │
   ▼
RSSCollector          ← feedparser
   │
   ▼
Summarizer            ← Ollama LLM (deepseek-r1)
   │
   ▼
Deduplicator          ← sentence-transformers (all-MiniLM-L6-v2) + cosine similarity
   │
   ▼
Classifier            ← Ollama LLM → JSON category list
   │
   ▼
NewsRankingAgent      ← Ollama LLM → JSON score breakdown
   │
   ▼
PostgreSQL            ← SQLAlchemy persistence
   │
   ▼
NewsletterBuilder     ← HTML email
   │
   ▼
EmailSender           ← SMTP (Gmail)
```

## Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/) installed and running locally
- PostgreSQL database
- Redis (broker + result backend)
- A compatible LLM pulled (default: `deepseek-r1:latest`)

```bash
ollama pull deepseek-r1:latest
```

## Installation

```bash
git clone https://github.com/your-username/AI-News-Aggregator.git
cd AI-News-Aggregator
pip install -r requirements.txt
```

## Configuration

Copy `.env` and fill in your values:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

MODEL_NAME=deepseek-r1:latest
MODEL_TEMPERATURE=0.2
MODEL_CONTEXT_WINDOW=8192

DATABASE_URL=postgresql://postgres:password@localhost:5432/news

BROKER_URL=redis://localhost:6379/0
RESULT_BACKEND=redis://localhost:6379/0
```

RSS feeds and other app-level settings are configured in `app/config.py`:

| Variable | Default | Description |
|---|---|---|
| `RSS_FEEDS` | OpenAI blog | Dict of `{source_name: rss_url}` |
| `MODEL_NAME` | `deepseek-r1:latest` | Ollama model to use |
| `MODEL_TEMPERATURE` | `0.2` | LLM temperature |
| `MODEL_CONTEXT_WINDOW` | `8192` | LLM context window |

## Running

### Docker (recommended)

```bash
docker-compose up --build
```

Starts the API on port `8001`, a Celery worker, PostgreSQL, and Redis.

### Local — API Server

```bash
uvicorn app.api.main:app --reload
```

### Local — Celery Worker

```bash
celery -A app.workers.celery_app worker --loglevel=info
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/run-pipeline` | Trigger full collect → rank → persist pipeline (async) |
| `POST` | `/send-newsletter` | Send newsletter from stored articles (async) |
| `GET` | `/news` | Latest 20 articles |
| `GET` | `/news/top?limit=5` | Top N articles |
| `GET` | `/news/category/{category}` | Filter articles by category |

Pipeline tasks run via Celery and return a `task_id` for status tracking.

## Pipeline Details

1. **Collect** — Fetches up to 5 articles per RSS source via `feedparser`.
2. **Summarize** — Sends raw content to the local Ollama LLM for concise summarization.
3. **Deduplicate** — Batch-encodes articles with `all-MiniLM-L6-v2`, removes near-duplicates using cosine similarity (threshold: 0.92).
4. **Classify** — LLM assigns up to 3 categories per article.
5. **Rank** — LLM scores each article across 5 dimensions: `technical_impact`, `industry_importance`, `recency`, `ai_relevance`, `source_credibility`.
6. **Persist** — Articles saved to PostgreSQL via SQLAlchemy.
7. **Newsletter** — Top articles rendered into HTML and sent via Gmail SMTP.

## Dependencies

| Package | Purpose |
|---|---|
| `feedparser` | RSS feed parsing |
| `ollama` | Local LLM inference |
| `fastapi` + `uvicorn[standard]` | REST API |
| `celery[redis]` | Async task queue |
| `redis` | Celery broker & result backend |
| `sqlalchemy` + `psycopg2-binary` | PostgreSQL ORM |
| `sentence-transformers` | Semantic embeddings for deduplication |
| `scikit-learn` | Cosine similarity |
| `pydantic` | Data validation |
| `python-dotenv` | Environment variable loading |
| `numpy` | Numerical operations |
