from sklearn.metrics.pairwise import cosine_similarity
from app.embeddings.encoder import EmbeddingEncoder


class Deduplicator:
    """
    Removes near-duplicate articles using semantic similarity.
    """

    def __init__(self, threshold: float = 0.92):
        self.encoder = EmbeddingEncoder()
        self.threshold = threshold
        self.embeddings = []          # Store embeddings of unique articles
        self.unique_articles = []     # Keep reference to original articles

    def remove_duplicates(self, articles):
        """
        Remove duplicate articles based on semantic similarity.
        """
        if not articles:
            return []

        # Batch encode all articles at once (much faster)
        texts = []
        valid_articles = []

        for article in articles:
            text = self._get_text(article)
            if text and text.strip():
                texts.append(text)
                valid_articles.append(article)

        if not texts:
            return []

        # Batch encoding = big performance boost
        print(f"Encoding {len(texts)} articles for deduplication...")
        embeddings = self.encoder.encode_batch(texts)

        unique_articles = []
        unique_embeddings = []

        for article, embedding in zip(valid_articles, embeddings):
            is_duplicate = False

            # Compare with existing unique articles
            if len(unique_embeddings) > 0:
                similarities = cosine_similarity(
                    [embedding], 
                    unique_embeddings
                )[0]

                if similarities.max() >= self.threshold:
                    is_duplicate = True

            if not is_duplicate:
                unique_articles.append(article)
                unique_embeddings.append(embedding)

        print(f"Deduplication complete: {len(articles)} → {len(unique_articles)} articles")
        
        return unique_articles

    def _get_text(self, article):
        """Extract best available text for comparison"""
        # Priority: summary > content > title
        if hasattr(article, 'summary') and article.summary:
            return article.summary
        elif hasattr(article, 'content') and article.content:
            return article.content[:2000]  # Limit length for efficiency
        elif hasattr(article, 'title') and article.title:
            return article.title
        return ""