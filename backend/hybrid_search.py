
from backend.keyword_search import KeywordSearch
from backend.semantic_search import SemanticSearch
from backend.reranker import DocumentReranker


class HybridSearch:
    """Combine BM25 and semantic retrieval, then rerank candidates."""

    def __init__(self):
        self.keyword_search = KeywordSearch()
        self.semantic_search = SemanticSearch()
        self.reranker = DocumentReranker()

    def build_index(self, chunks: list[dict]) -> None:
        """Build both retrieval indexes from the same chunks."""
        self.keyword_search.build_index(chunks)
        self.semantic_search.build_index(chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Retrieve candidates with RRF and rerank them."""
        if self.keyword_search.index is None:
            raise ValueError("Build the index before searching.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        if not query.strip():
            return []

        candidate_k = min(max(top_k * 3, 10), 30)

        keyword_results = self.keyword_search.search(
            query,
            top_k=candidate_k,
        )
        semantic_results = self.semantic_search.search(
            query,
            top_k=candidate_k,
        )

        # Combine keyword and semantic rankings using RRF.
        rrf_scores = {}
        chunk_lookup = {}
        rrf_constant = 60

        for ranked_results in (keyword_results, semantic_results):
            for rank, chunk in enumerate(ranked_results, start=1):
                chunk_id = chunk["chunk_id"]

                rrf_scores[chunk_id] = (
                    rrf_scores.get(chunk_id, 0.0)
                    + 1.0 / (rrf_constant + rank)
                )
                chunk_lookup[chunk_id] = chunk

        ranked_ids = sorted(
            rrf_scores,
            key=rrf_scores.get,
            reverse=True,
        )

        candidates = [
            {
                **chunk_lookup[chunk_id],
                "rrf_score": float(rrf_scores[chunk_id]),
            }
            for chunk_id in ranked_ids[:candidate_k]
        ]

        # Rerank the combined candidates with the cross-encoder.
        reranked_results = self.reranker.rerank(
            query,
            candidates,
            top_k=top_k,
        )

        # The primary score now represents the final reranker score.
        return [
            {
                **result,
                "score": result["rerank_score"],
            }
            for result in reranked_results
        ]
