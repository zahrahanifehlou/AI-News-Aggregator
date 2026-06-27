RANKING_PROMPT = """
You are an expert AI news ranking system.

Your job is to score the importance of an article for an AI/ML engineer.

Return STRICT JSON only.

Scoring rules (total 100):

- Technical Impact (0–25)
- Industry Importance (0–25)
- Recency / Breaking News (0–20)
- AI/ML Relevance (0–20)
- Source Credibility (0–10)

Article Title:
{title}

Summary:
{summary}

Categories:
{categories}

Return format:
{
  "technical_impact": 0,
  "industry_importance": 0,
  "recency": 0,
  "ai_relevance": 0,
  "source_credibility": 0,
  "total": 0
}
"""