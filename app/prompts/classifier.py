CLASSIFICATION_PROMPT = """
You are an AI news classifier.

Task:
Assign relevant categories to the article.

Rules:
- Choose ONLY from the allowed categories.
- Return a JSON array.
- Maximum 3 categories per article.
- If unsure, return ["AI Research"].

Allowed categories:
{categories}

Article Title:
{title}

Article Summary:
{summary}

Return format (STRICT JSON):
["Category1", "Category2"]
"""