from sentence_transformers import SentenceTransformer


class MultilingualEmbedder:
    def __init__(self, model_name: str = "BAAI/bge-m3", device: str = "cpu"):
        print(f"Loading embedding model: {model_name} on {device}...")
        self.model = SentenceTransformer(model_name, device=device)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Convert a batch of chunks into normalized 1024-dim vectors."""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return [vec.tolist() for vec in embeddings]

    def embed_query(self, query: str) -> list[float]:
        """Convert a single search query into a normalized 1024-dim vector."""
        return self.embed_texts([query])[0]
