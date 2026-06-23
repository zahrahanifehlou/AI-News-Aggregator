"""Generate summaries for collected content."""

import logging

from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def _extractive_summary(text: str | None, max_sentences: int = 3) -> str:
    """Fallback summarizer that returns the first few sentences."""
    if not text:
        return "No content available to summarize."
    sentences = [s.strip() for s in text.split(". ") if s.strip()]
    return ". ".join(sentences[:max_sentences]).rstrip(".") + "."


def generate_summary(text: str | None, title: str | None = None) -> str:
    """Generate a summary using OpenAI if configured, otherwise fallback."""
    if not settings.openai_api_key:
        return _extractive_summary(text, max_sentences=3)

    try:
        import openai
    except ImportError:
        logger.warning("openai package not installed; using fallback summary")
        return _extractive_summary(text, max_sentences=3)

    client = openai.OpenAI(api_key=settings.openai_api_key)
    prompt = (
        f"Summarize the following article in no more than {settings.summary_max_length} words.\n\n"
    )
    if title:
        prompt += f"Title: {title}\n\n"
    prompt += f"Content: {text or 'No content available'}"

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise news summarizer. Respond with a single paragraph summary.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )
        summary = response.choices[0].message.content.strip()
        return summary or _extractive_summary(text, max_sentences=3)
    except Exception as exc:
        logger.error("OpenAI summarization failed: %s", exc)
        return _extractive_summary(text, max_sentences=3)
