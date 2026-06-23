"""Application configuration loaded from environment variables."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ainews"

    # Scheduler
    collection_interval_minutes: int = 60
    summary_send_hour: int = 8
    summary_send_minute: int = 0
    timezone: str = "UTC"

    # OpenAI summarization
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    summary_max_length: int = 250

    # Email (SMTP)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    smtp_to: str | None = None
    smtp_tls: bool = True

    # Application
    log_level: str = "INFO"
    days_to_keep: int = 30

    @property
    def sender_email(self) -> str:
        return self.smtp_from or self.smtp_user or "ai-news-aggregator@localhost"

    @property
    def recipient_emails(self) -> list[str]:
        if not self.smtp_to:
            return []
        return [email.strip() for email in self.smtp_to.split(",") if email.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
