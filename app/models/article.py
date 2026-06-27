from dataclasses import dataclass


@dataclass
class Article:
    title: str
    content: str
    url: str
    published_at: str
    source: str
    summary: str = ""
    categories: list[str] = None
    score: float = 0.0
    score_breakdown: dict = None

    def __repr__(self):
        return f"Article(title='{self.title}', source='{self.source}', score={self.score}, summary_len={len(self.summary)}, categories={self.categories}, content_len={len(self.content)})"

    def __str__(self):
        return f"[{self.source}] {self.title}"