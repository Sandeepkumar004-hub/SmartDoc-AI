
from io import BytesIO

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def create_test_pdf() -> bytes:
    """Create a small valid PDF for upload tests."""
    import pymupdf

    pdf_bytes = BytesIO()

    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Python machine learning data analysis",
    )

    pdf_bytes.write(document.tobytes())
    document.close()

    return pdf_bytes.getvalue()


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_search_without_upload_returns_400():
    # Reset the in-memory index for this test.
    import backend.main as main

    main.keyword_search = main.KeywordSearch()
    main.current_filename = None

    response = client.post(
        "/search",
        json={"query": "Python", "top_k": 5},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Upload a PDF before searching."


def test_upload_pdf_and_search():
    import backend.main as main

    main.keyword_search = main.KeywordSearch()
    main.current_filename = None

    pdf_content = create_test_pdf()

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "test_document.pdf",
                pdf_content,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 200

    upload_data = upload_response.json()
    assert upload_data["filename"] == "test_document.pdf"
    assert upload_data["chunk_count"] >= 1

    search_response = client.post(
        "/search",
        json={"query": "Python", "top_k": 5},
    )

    assert search_response.status_code == 200

    search_data = search_response.json()
    assert search_data["filename"] == "test_document.pdf"
    assert search_data["result_count"] >= 1
    assert "Python" in search_data["results"][0]["text"]


def test_upload_rejects_non_pdf_file():
    response = client.post(
        "/upload",
        files={
            "file": (
                "notes.txt",
                b"This is not a PDF.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a PDF file."

def test_search_rejects_empty_query():
    response = client.post(
        "/search",
        json={"query": "", "top_k": 5},
    )

    assert response.status_code == 422


def test_search_rejects_invalid_top_k():
    response = client.post(
        "/search",
        json={"query": "Python", "top_k": 0},
    )

    assert response.status_code == 422


def test_upload_rejects_invalid_pdf_content():
    response = client.post(
        "/upload",
        files={
            "file": (
                "broken.pdf",
                b"This is not a valid PDF document.",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The uploaded file is not a valid PDF."
