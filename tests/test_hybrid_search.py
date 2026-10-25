
import pytest

from backend.hybrid_search import HybridSearch


@pytest.fixture
def sample_chunks():
    return [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": (
                "React and Node.js are used to build "
                "full-stack web applications."
            ),
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": (
                "SQL is useful for analyzing sales data "
                "and business performance."
            ),
        },
        {
            "chunk_id": 3,
            "page_number": 3,
            "text": (
                "Seismic waves help researchers study "
                "earthquakes and ground motion."
            ),
        },
    ]


@pytest.fixture
def hybrid_search(sample_chunks):
    search = HybridSearch()
    search.build_index(sample_chunks)
    return search


def test_search_requires_index():
    search = HybridSearch()

    with pytest.raises(ValueError, match="Build the index"):
        search.search("web applications")


def test_build_index_rejects_empty_chunks():
    search = HybridSearch()

    with pytest.raises(ValueError, match="No searchable text"):
        search.build_index([])


def test_hybrid_search_returns_results(hybrid_search):
    results = hybrid_search.search("React web application")

    assert len(results) > 0
    assert all("score" in result for result in results)
    assert all("text" in result for result in results)


def test_hybrid_search_respects_top_k(hybrid_search):
    results = hybrid_search.search("data analysis", top_k=2)

    assert len(results) == 2


def test_hybrid_search_empty_query_returns_empty_list(hybrid_search):
    assert hybrid_search.search("   ") == []


def test_hybrid_search_rejects_invalid_top_k(hybrid_search):
    with pytest.raises(ValueError, match="top_k"):
        hybrid_search.search("React", top_k=0)


def test_hybrid_results_have_unique_chunk_ids(hybrid_search):
    results = hybrid_search.search("web development and SQL")

    chunk_ids = [result["chunk_id"] for result in results]

    assert len(chunk_ids) == len(set(chunk_ids))
