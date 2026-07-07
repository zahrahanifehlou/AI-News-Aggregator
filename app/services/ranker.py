import json
from app.llm.provider import LLMProvider
from app.prompts.ranker import RANKING_PROMPT


class NewsRankingAgent:

    def rank(self, article):

        prompt = RANKING_PROMPT.format(
            title=article.title,
            summary=article.summary,
            categories=article.categories
        )

        response = LLMProvider.classify(prompt)

        response = response.strip()
        if response.startswith("```json"):
            response = response.split("```json")[1].split("```")[0].strip()
        elif response.startswith("```"):
            response = response.split("```")[1].split("```")[0].strip()

        try:
            scores = json.loads(response)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Ranking parse error for '{article.title}': {e}")
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