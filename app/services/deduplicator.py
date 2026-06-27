from sklearn.metrics.pairwise import cosine_similarity
from app.embeddings.encoder import EmbeddingEncoder

class Deduplicator:

    def __init__(self, threshold=0.85):
        self.encoder = EmbeddingEncoder()
        self.threshold = threshold

    def remove_duplicates(self, articles):

        unique_articles = []
        embeddings = []

        for article in articles:

            embedding = self.encoder.encode(article.summary)

            duplicate = False

            for existing_embedding in embeddings:

                similarity = cosine_similarity(
                    [embedding],
                    [existing_embedding]
                )[0][0]

                if similarity >= self.threshold:
                    duplicate = True
                    break

            if not duplicate:
                unique_articles.append(article)
                embeddings.append(embedding)

        return unique_articles