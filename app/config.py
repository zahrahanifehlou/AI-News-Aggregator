import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# RSS feeds (application constant)
# -----------------------------
RSS_FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    # "HuggingFace": "https://huggingface.co/blog/feed.xml",
}

# -----------------------------
# LLM Settings
# -----------------------------
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-r1:latest")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", 0.2))
MODEL_CONTEXT_WINDOW = int(os.getenv("MODEL_CONTEXT_WINDOW", 8192))

# -----------------------------
# Database
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# -----------------------------
# Email
# -----------------------------
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# -----------------------------
# Celery
# -----------------------------
BROKER_URL = os.getenv("BROKER_URL")
RESULT_BACKEND = os.getenv("RESULT_BACKEND")

# # ollama list
# # NAME                        ID              SIZE      MODIFIED
# # gemma4:latest               c6eb396dbd59    9.6 GB    2 months ago
# # qwen3.5:27b                 7653528ba5cb    17 GB     3 months ago
# # qwen35-uncensored:latest    443fb05972d8    6.7 GB    3 months ago
# # deepseek-r1:latest          6995872bfe4c    5.2 GB    3 months ago
# # deepseek-r1:8b              6995872bfe4c    5.2 GB    3 months ago
# # codestral:latest            0898a8b286d5    12 GB     3 months ago
# # devstral-2:latest           524a6607f0f5    74 GB     3 months ago
# # qwen3-coder-next:latest     ca06e9e4087c    51 GB     4 months ago
# # deepseek-coder:33b          acec7c0b0fd9    18 GB     4 months ago
# # qwen3-coder:latest          06c1097efce0    18 GB     4 months ago
