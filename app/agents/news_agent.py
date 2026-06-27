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

        response = self.llm.generate(prompt)

        
        try:
            scores = json.loads(response)
        except:
            scores = {
                "technical_impact": 0,
                "industry_importance": 0,
                "recency": 0,
                "ai_relevance": 0,
                "source_credibility": 0,
                "total": 0
            }

        article.score_breakdown = scores
        article.score = scores.get("total", 0)

        return article