# SmartDoc AI — Hybrid RAG with Reranking

SmartDoc AI is a full-stack document search application that lets users upload PDF files and retrieve relevant passages using hybrid search and cross-encoder reranking.

## Features

- **PDF Processing:** Extract text from PDF documents while preserving page numbers.
- **Text Chunking:** Split extracted text into overlapping chunks for retrieval.
- **BM25 Keyword Search:** Retrieve passages based on keyword relevance.
- **Semantic Search:** Generate text embeddings using Sentence Transformers.
- **Hybrid Retrieval:** Combine keyword and semantic rankings using Reciprocal Rank Fusion (RRF).
- **Cross-Encoder Reranking:** Reorder retrieved candidates based on query-document relevance.
- **REST API:** FastAPI endpoints for uploading PDFs and searching documents.
- **Frontend:** React and TypeScript interface for document upload and search.
- **Automated Tests:** Test coverage for PDF processing APIs, keyword search, semantic search, hybrid retrieval, and reranking.

## Technology Stack

**Frontend:** React, TypeScript, Vite, CSS

**Backend:** Python, FastAPI, Uvicorn

**Retrieval and ML:** BM25, Sentence Transformers, Cross-Encoder, NumPy

**PDF Processing:** PyMuPDF

**Testing:** Pytest, HTTPX

## Project Architecture

1. Upload a PDF through the frontend.
2. Extract text and preserve page numbers.
3. Split the text into overlapping chunks.
4. Build a BM25 index and generate semantic embeddings.
5. Retrieve candidate passages using both search methods.
6. Combine rankings using Reciprocal Rank Fusion.
7. Rerank candidates using a cross-encoder model.
8. Return ranked passages and their scores through the API.

## Project Structure

```text
SmartDoc-AI/
├── backend/
│   ├── main.py
│   ├── pdf_processor.py
│   ├── chunker.py
│   ├── keyword_search.py
│   ├── semantic_search.py
│   ├── hybrid_search.py
│   └── reranker.py
├── frontend/
├── tests/
│   ├── test_api.py
│   ├── test_keyword_search.py
│   ├── test_semantic_search.py
│   ├── test_hybrid_search.py
│   └── test_reranker.py
├── sample_data/
├── docs/
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12 recommended
- Node.js and npm
- Git
- Internet access for the initial download of the machine-learning models

## Backend Setup

From the project root, create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
python -m pip install fastapi "uvicorn[standard]" python-multipart pymupdf rank-bm25 sentence-transformers numpy pytest httpx
```

Start the backend:

```powershell
python -m uvicorn backend.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

## Frontend Setup

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local Vite URL displayed in the terminal, usually http://localhost:5173/.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| POST | `/upload` | Upload and index a PDF |
| POST | `/search` | Search the indexed document |

Example search request:

```json
{
  "query": "frontend web application development",
  "top_k": 5
}
```

Search results include the retrieved text, page and chunk metadata, the RRF score, and the cross-encoder reranking score.

## Run Tests

From the project root with the virtual environment activated:

```powershell
python -m pytest -v
```

The project currently passes 34 automated tests in the local development environment.

## Current Limitations

- The application keeps the active document index in memory; restarting the backend clears it.
- The current workflow is designed around one active PDF index at a time.
- Scanned PDFs without extractable text may require OCR.
- The first model initialization requires downloading the embedding and reranking models.
- Retrieval quality depends on document text, chunking, query wording, and the selected models.

## Future Improvements

- Support multiple documents and persistent indexes.
- Add OCR for scanned PDFs.
- Improve retrieval evaluation with a labeled query dataset and ranking metrics.
- Add document-level metadata filtering and richer citations.
- Add production deployment, authentication, and monitoring.

## Author

**Sandeep Kumar**

GitHub: https://github.com/Sandeepkumar004-hub

---

*This project was developed as a hands-on exploration of document retrieval, semantic embeddings, hybrid search, and reranking.*