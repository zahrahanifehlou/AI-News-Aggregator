import os
from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# RSS feeds (application constants)
# -----------------------------
RSS_FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
}


# -----------------------------
# LLM Settings
# -----------------------------
OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://127.0.0.1:11434"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "deepseek-r1:latest"
)

MODEL_TEMPERATURE = float(
    os.getenv(
        "MODEL_TEMPERATURE",
        "0.2"
    )
)

MODEL_CONTEXT_WINDOW = int(
    os.getenv(
        "MODEL_CONTEXT_WINDOW",
        "8192"
    )
)


# -----------------------------
# Database
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# -----------------------------
# Email
# -----------------------------
EMAIL_USER = os.getenv(
    "EMAIL_USER"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)
TO_EMAIL = os.getenv(
    "TO_EMAIL"
)

# -----------------------------
# Celery
# -----------------------------
BROKER_URL = os.getenv(
    "BROKER_URL",
    "redis://redis:6379/0"
)

RESULT_BACKEND = os.getenv(
    "RESULT_BACKEND",
    "redis://redis:6379/0"
)