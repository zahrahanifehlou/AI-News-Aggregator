from dataclasses import dataclass


@dataclass
class Article:
    """
    Standardized news article format used across all collectors.
    """

    title: str
    summary: str
    url: str
    published_at: str
    source: str