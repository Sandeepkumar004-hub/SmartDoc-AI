
from sentence_transformers import CrossEncoder


class DocumentReranker:
    """Rerank retrieved document chunks using a cross-encoder."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:
        """Sort candidate documents by query-document relevance."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        if not query.strip() or not documents:
            return []

        pairs = [
            (query, document["text"])
            for document in documents
            if document.get("text", "").strip()
        ]

        valid_documents = [
            document
            for document in documents
            if document.get("text", "").strip()
        ]

        if not valid_documents:
            return []

        scores = self.model.predict(pairs)

        ranked_documents = []

        for document, score in zip(valid_documents, scores):
            ranked_documents.append(
                {
                    **document,
                    "rerank_score": float(score),
                }
            )

        ranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return ranked_documents[:top_k]
