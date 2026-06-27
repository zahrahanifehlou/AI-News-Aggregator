from sentence_transformers import SentenceTransformer


class EmbeddingEncoder:
    def __init__(self):
        # You can make model name configurable later
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Embedding model loaded successfully")

    def encode(self, text: str):
        if not text or not isinstance(text, str):
            return None
        return self.model.encode(text, convert_to_numpy=True)

    def encode_batch(self, texts: list[str]):
        """Bonus: batch encoding for better performance"""
        if not texts:
            return None
        return self.model.encode(texts, convert_to_numpy=True)