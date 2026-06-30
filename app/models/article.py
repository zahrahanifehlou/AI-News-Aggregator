from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Article:
    """A single news article flowing through the collection pipeline."""

    title: str
    content: str
    url: str
    published_at: str
    source: str
    summary: str = ""
    categories: list[str] = field(default_factory=list)
    score: float = 0.0
    score_breakdown: dict[str, float] = field(default_factory=dict)

    def __repr__(self) -> str:
        return (
            f"Article(title={self.title!r}, source={self.source!r}, "
            f"score={self.score}, summary_len={len(self.summary)}, "
            f"categories={self.categories}, content_len={len(self.content)})"
        )

    def __str__(self) -> str:
        return f"[{self.source}] {self.title}"
