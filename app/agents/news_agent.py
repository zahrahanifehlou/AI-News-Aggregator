import json
from app.llm.provider import LLMProvider
from app.prompts.ranker import RANKING_PROMPT


class NewsRankingAgent:

    def __init__(self):
        self.llm = LLMProvider()

    def rank(self, article):

        prompt = RANKING_PROMPT.format(
            title=article.title,
            summary=article.summary,
            categories=article.categories
        )

        response = self.llm.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        raw = response.choices[0].message.content

        try:
            scores = json.loads(raw)
        except:
            scores = {
                "technical_impact": 10,
                "industry_importance": 10,
                "recency": 10,
                "ai_relevance": 10,
                "source_credibility": 5,
                "total": 45
            }

        article.score_breakdown = scores
        article.score = scores.get("total", 0)

        return article