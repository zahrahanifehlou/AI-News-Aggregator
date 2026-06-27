from sentence_transformers import SentenceTransformer


class EmbeddingEncoder:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )
        print("✅ Embedding model loaded successfully")

    def encode(self, text: str):
        return self.model.encode(text)