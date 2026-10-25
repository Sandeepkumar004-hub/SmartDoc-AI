
import re
from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


class KeywordSearch:
    def __init__(self):
        self.chunks = []
        self.index = None

    def build_index(self, chunks: list[dict]) -> None:
        """Build a BM25 index from document chunks."""
        valid_chunks = [
            chunk
            for chunk in chunks
            if chunk.get("text", "").strip()
        ]

        if not valid_chunks:
            raise ValueError("No searchable text chunks provided.")

        tokenized_chunks = [
            tokenize(chunk["text"])
            for chunk in valid_chunks
        ]

        self.chunks = valid_chunks
        self.index = BM25Okapi(tokenized_chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Return matching chunks ranked by BM25 score."""
        if self.index is None:
            raise ValueError("Build the index before searching.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_tokens = tokenize(query)

        if not query_tokens:
            return []

        scores = self.index.get_scores(query_tokens)
        query_terms = set(query_tokens)
        results = []

        for index, score in enumerate(scores):
            chunk = self.chunks[index]
            chunk_tokens = set(tokenize(chunk["text"]))

            # Skip chunks that contain none of the query words.
            if not query_terms.intersection(chunk_tokens):
                continue

            results.append({
                **chunk,
                "score": float(score),
            })

        # Rank the matching chunks by BM25 score.
        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results[:top_k]
