from app.llm.provider import LLMProvider


class Summarizer:

    def summarize(self, article):

        summary = LLMProvider.summarize(article.content)

        article.summary = summary

        return article