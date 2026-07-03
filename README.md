# AI News Aggregator

An automated AI news collection, summarization, ranking, and newsletter delivery pipeline powered by local LLMs via [Ollama](https://ollama.com/).

## Overview

This project fetches articles from RSS feeds, summarizes and deduplicates them using semantic embeddings, classifies them into AI-relevant categories, scores them with an LLM-based ranking agent, and delivers a curated HTML newsletter via email — all exposed through a FastAPI REST API.

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
NewsletterBuilder     ← HTML email
   │
   ▼
EmailSender           ← SMTP delivery
```

## Project Structure

```
AI-News-Aggregator/
├── app/
│   ├── agents/
│   │   └── news_agent.py        # LLM-based article ranking agent
│   ├── api/
│   │   └── main.py              # FastAPI app & route definitions
│   ├── collectors/
│   │   └── rss.py               # RSS feed collector
│   ├── embeddings/
│   │   └── encoder.py           # Sentence-transformer embedding encoder
│   ├── llm/
│   │   └── provider.py          # Ollama LLM wrapper
│   ├── models/
│   ├── prompts/                 # LLM prompt templates
│   ├── services/
│   │   ├── classifier.py        # Article category classifier
│   │   ├── deduplicator.py      # Semantic deduplication
│   │   ├── email_sender.py      # SMTP email sender
│   │   ├── newsletter.py        # HTML newsletter builder
│   │   ├── pipeline.py          # End-to-end pipeline orchestration
│   │   ├── summarizer.py        # Article summarizer
│   │   └── taxonomy.py          # Category taxonomy definitions
│   ├── config.py                # Config (feeds, model, DB, email)
│   └── main.py                  # CLI entrypoint
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally
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

Edit `.env` and set your email credentials:

```env
EMAIL_USER=your_email@example.com
EMAIL_PASSWORD=your_email_password
```

Additional settings in `app/config.py`:

| Variable | Default | Description |
|---|---|---|
| `RSS_FEEDS` | OpenAI blog | Dict of `{source_name: rss_url}` |
| `model_name` | `deepseek-r1:latest` | Ollama model to use |
| `model_temperature` | `0.2` | LLM temperature |
| `model_context_window` | `8192` | LLM context window |
| `DATABASE_URL` | PostgreSQL local | Database connection string |

## Running

### CLI (one-shot)

```bash
python -m app.main
```

### API Server

```bash
uvicorn app.api.main:app --reload
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/health` | Service status + article count |
| `POST` | `/run-pipeline` | Run full collection → ranking pipeline |
| `POST` | `/send-newsletter` | Send newsletter from latest pipeline results |
| `GET` | `/news` | List all articles (sorted by score) |
| `GET` | `/news/top?limit=5` | Top N ranked articles |
| `GET` | `/news/category/{category}` | Filter articles by category |

## Pipeline Details

1. **Collect** — Fetches articles from configured RSS feeds via `feedparser`.
2. **Summarize** — Sends raw article content to the local Ollama LLM for concise summarization.
3. **Deduplicate** — Encodes all articles with `all-MiniLM-L6-v2` and removes near-duplicates using cosine similarity (threshold: 0.92).
4. **Classify** — LLM assigns up to 3 categories per article from the taxonomy defined in `taxonomy.py`.
5. **Rank** — LLM scores each article across 5 dimensions: `technical_impact`, `industry_importance`, `recency`, `ai_relevance`, `source_credibility`, producing a final `total` score.
6. **Newsletter** — Top articles are rendered into an HTML email and sent via SMTP.

## Dependencies

| Package | Purpose |
|---|---|
| `feedparser` | RSS feed parsing |
| `ollama` | Local LLM inference |
| `fastapi` + `uvicorn` | REST API |
| `sentence-transformers` | Semantic embeddings for deduplication |
| `scikit-learn` | Cosine similarity |
| `pydantic` | Data models |
| `python-dotenv` | Environment variable loading |
| `numpy` | Numerical operations |
