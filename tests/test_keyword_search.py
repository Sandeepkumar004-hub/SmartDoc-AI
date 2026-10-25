
import pytest

from backend.keyword_search import KeywordSearch, tokenize


@pytest.fixture
def sample_chunks():
    """Provide sample document chunks for testing."""
    return [
        {
            "chunk_id": 1,
            "page_number": 1,
            "text": "Python is used for machine learning and data analysis.",
        },
        {
            "chunk_id": 2,
            "page_number": 2,
            "text": "CampusEase is a student service platform built with MERN.",
        },
        {
            "chunk_id": 3,
            "page_number": 3,
            "text": "Machine learning models use data to make predictions.",
        },
    ]


@pytest.fixture
def search_engine(sample_chunks):
    """Create a keyword search index for the sample chunks."""
    engine = KeywordSearch()
    engine.build_index(sample_chunks)
    return engine


def test_tokenize_converts_text_to_lowercase():
    assert tokenize("Python MACHINE Learning") == [
        "python",
        "machine",
        "learning",
    ]


def test_build_index_stores_chunks(search_engine, sample_chunks):
    assert len(search_engine.chunks) == len(sample_chunks)
    assert search_engine.index is not None


def test_search_returns_matching_chunks(search_engine):
    results = search_engine.search("machine learning", top_k=5)

    assert len(results) > 0
    assert all("score" in result for result in results)

    matching_text = " ".join(
        result["text"].lower() for result in results
    )
    assert "machine learning" in matching_text


def test_search_respects_top_k(search_engine):
    results = search_engine.search("data", top_k=1)
    assert len(results) <= 1


def test_empty_query_returns_no_results(search_engine):
    assert search_engine.search("   ") == []


def test_search_before_indexing_raises_error():
    engine = KeywordSearch()

    with pytest.raises(ValueError, match="Build the index"):
        engine.search("python")


def test_build_index_rejects_empty_chunks():
    engine = KeywordSearch()

    with pytest.raises(ValueError, match="No searchable text chunks"):
        engine.build_index([])
