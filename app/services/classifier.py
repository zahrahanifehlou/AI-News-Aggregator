import json
from app.llm.provider import LLMProvider
from app.prompts.classifier import CLASSIFICATION_PROMPT
from app.services.taxonomy import CATEGORIES


class Classifier:

    def __init__(self):
        self.llm = LLMProvider()

    def classify(self, article):
        """
        Classify article into categories using local Ollama model.
        """
        # Prepare prompt
        prompt = CLASSIFICATION_PROMPT.format(
            categories=", ".join(CATEGORIES),
            title=article.title or "",
            summary=article.summary or article.content[:1000] or ""  # fallback
        )

        try:
            raw_output = self.llm.classify(prompt)

            # Clean possible markdown/code block wrappers
            raw_output = raw_output.strip()
            if raw_output.startswith("```json"):
                raw_output = raw_output.split("```json")[1].split("```")[0]
            elif raw_output.startswith("```"):
                raw_output = raw_output.split("```")[1].split("```")[0]

            # Parse JSON
            categories = json.loads(raw_output)

            # Ensure it's a list
            if isinstance(categories, str):
                categories = [categories]
            elif not isinstance(categories, list):
                categories = ["AI Research"]

        except Exception as e:
            print(f"Classification error for '{article.title}': {e}")
            categories = ["AI Research"]  # safe fallback

        # Optional: Limit to max 3 categories
        article.categories = categories[:3]
        return article