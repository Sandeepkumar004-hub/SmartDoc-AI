
import pytest

from backend.reranker import DocumentReranker


@pytest.fixture(scope="module")
def reranker():
    return DocumentReranker()


@pytest.fixture
def sample_documents():
    return [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": "The weather is sunny and warm today.",
            "score": 0.8,
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": (
                "Python is a programming language used "
                "for software development and data analysis."
            ),
            "score": 0.5,
        },
        {
            "chunk_id": 3,
            "page_number": 3,
            "text": "Fresh vegetables are rich in vitamins.",
            "score": 0.3,
        },
    ]


def test_rerank_returns_results(reranker, sample_documents):
    results = reranker.rerank(
        "Which programming language is used for software development?",
        sample_documents,
    )

    assert len(results) == 3
    assert all("rerank_score" in item for item in results)


def test_rerank_places_relevant_document_first(
    reranker,
    sample_documents,
):
    results = reranker.rerank(
        "Which programming language is used for software development?",
        sample_documents,
    )

    assert results[0]["chunk_id"] == 2


def test_rerank_respects_top_k(reranker, sample_documents):
    results = reranker.rerank(
        "Python programming",
        sample_documents,
        top_k=2,
    )

    assert len(results) == 2


def test_rerank_empty_query_returns_empty_list(reranker):
    assert reranker.rerank("  ", []) == []


def test_rerank_rejects_invalid_top_k(reranker, sample_documents):
    with pytest.raises(ValueError, match="top_k"):
        reranker.rerank("Python", sample_documents, top_k=0)


def test_rerank_ignores_empty_documents(reranker):
    documents = [
        {"chunk_id": 1, "text": ""},
        {
            "chunk_id": 2,
            "text": "Python is used for programming.",
        },
    ]

    results = reranker.rerank("Python programming", documents)

    assert len(results) == 1
    assert results[0]["chunk_id"] == 2
