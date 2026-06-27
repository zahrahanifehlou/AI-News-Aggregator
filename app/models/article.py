from dataclasses import dataclass


@dataclass
class Article:
    """
    Standardized news article format used across all collectors.
    """
    title: str
    content: str
    url: str
    published_at: str
    source: str
    summary: str = ""
    categories: list[str] = None