
import pytest

from backend.semantic_search import SemanticSearch


@pytest.fixture(scope="module")
def semantic_search():
    """Load the embedding model once for this test module."""
    return SemanticSearch()


@pytest.fixture
def sample_chunks():
    return [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": (
                "The student developed a web application using "
                "React, JavaScript, and Node.js."
            ),
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": (
                "Seismic waves are used to study earthquakes "
                "and predict ground motion."
            ),
        },
        {
            "chunk_id": 3,
            "page_number": 3,
            "text": (
                "SQL queries help analyze sales data and "
                "calculate business performance metrics."
            ),
        },
    ]


def test_search_requires_index(semantic_search):
    search = SemanticSearch()

    with pytest.raises(ValueError, match="Build the index"):
        search.search("web development")


def test_build_index_rejects_empty_chunks(semantic_search):
    with pytest.raises(ValueError, match="No searchable text"):
        semantic_search.build_index([])


def test_search_returns_results(semantic_search, sample_chunks):
    search = SemanticSearch()
    search.build_index(sample_chunks)

    results = search.search("frontend web application development")

    assert len(results) > 0
    assert results[0]["chunk_id"] in {1, 2, 3}
    assert isinstance(results[0]["score"], float)


def test_search_respects_top_k(semantic_search, sample_chunks):
    search = SemanticSearch()
    search.build_index(sample_chunks)

    results = search.search("data analysis", top_k=2)

    assert len(results) == 2


def test_search_empty_query_returns_empty_list(
    semantic_search,
    sample_chunks,
):
    search = SemanticSearch()
    search.build_index(sample_chunks)

    assert search.search("   ") == []


def test_search_rejects_invalid_top_k(semantic_search, sample_chunks):
    search = SemanticSearch()
    search.build_index(sample_chunks)

    with pytest.raises(ValueError, match="top_k"):
        search.search("web development", top_k=0)
