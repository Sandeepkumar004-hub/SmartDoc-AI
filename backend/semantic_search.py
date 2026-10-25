
from sentence_transformers import SentenceTransformer
import numpy as np


class SemanticSearch:
    """Search document chunks by semantic similarity."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None

    def build_index(self, chunks: list[dict]) -> None:
        """Create embeddings for the supplied document chunks."""
        valid_chunks = [
            chunk
            for chunk in chunks
            if chunk.get("text", "").strip()
        ]

        if not valid_chunks:
            raise ValueError("No searchable text chunks provided.")

        texts = [chunk["text"] for chunk in valid_chunks]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        self.chunks = valid_chunks
        self.embeddings = embeddings

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """Return chunks ranked by semantic similarity."""
        if self.embeddings is None:
            raise ValueError("Build the index before searching.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        if not query.strip():
            return []

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )[0]

        scores = self.embeddings @ query_embedding
        ranked_indices = np.argsort(scores)[::-1][:top_k]

        return [
            {
                **self.chunks[int(index)],
                "score": float(scores[index]),
            }
            for index in ranked_indices
        ]
