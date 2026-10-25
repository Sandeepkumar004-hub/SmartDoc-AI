
# SmartDoc AI — Intelligent PDF Search

A Python-based document search system that extracts text from PDFs, splits it into manageable chunks, and retrieves relevant information using BM25 keyword search.

## Overview

SmartDoc AI is a document-processing backend built with FastAPI. It allows users to upload PDF documents and search their contents through a REST API.

The project demonstrates document processing, text chunking, information retrieval, API development, and automated testing.

## Features

- **PDF Upload:** Accepts PDF files up to 10 MB.
- **Text Extraction:** Extracts text and preserves page numbers using PyMuPDF.
- **Text Chunking:** Splits extracted content into overlapping chunks.
- **Keyword Search:** Uses BM25 ranking to retrieve matching chunks.
- **REST API:** Provides endpoints through FastAPI.
- **Input Validation:** Handles invalid file types, oversized uploads, and invalid search requests.
- **Automated Tests:** Tests core search functionality and API behavior using pytest.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| PyMuPDF | PDF text extraction |
| rank-bm25 | Keyword retrieval |
| pytest | Automated testing |
| HTTPX | API testing support |

## Project Structure

```text
SmartDoc-AI/
├── backend/
│   ├── chunker.py
│   ├── keyword_search.py
│   ├── main.py
│   └── pdf_processor.py
├── tests/
│   ├── test_api.py
│   └── test_keyword_search.py
├── docs/
├── frontend/
├── sample_data/
├── README.md
└── .gitignore
```

## Getting Started

### 1. Prerequisites

- Python 3.12
- Git
- A terminal or VS Code

### 2. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartDoc-AI
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 3. Create a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install fastapi "uvicorn[standard]" pymupdf python-multipart rank-bm25 pytest httpx
```

### 5. Start the API

```powershell
python -m uvicorn backend.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/upload` | Upload, process, and index a PDF |
| POST | `/search` | Search the currently indexed PDF |

### Upload a PDF

Use `POST /upload` in Swagger UI and select a PDF file.

A successful response includes the filename, extracted page count, chunk count, and processing status.

### Search the document

First upload a PDF, then call `POST /search` with a JSON request body:

```json
{
  "query": "machine learning",
  "top_k": 5
}
```

The response contains matching chunks, page numbers, and BM25 scores.

## Run Tests

Run the complete automated test suite:

```powershell
python -m pytest -v
```

The current test suite covers keyword search, text tokenization, API endpoints, PDF uploads, and input validation.

## Current Limitations

- The search index is stored in memory and is cleared when the server restarts.
- Only the currently uploaded PDF is indexed.
- BM25 is keyword-based and does not understand semantic similarity.
- Scanned PDFs may require OCR to extract text.
- The frontend, semantic retrieval, reranking, and LLM-powered answers are planned future improvements.

## Roadmap

- [x] PDF text extraction
- [x] Text chunking
- [x] BM25 keyword search
- [x] FastAPI endpoints
- [x] Automated tests
- [ ] Semantic search with embeddings
- [ ] Hybrid retrieval
- [ ] Reranking
- [ ] LLM-generated answers with source citations
- [ ] React and TypeScript frontend
- [ ] Persistent document storage

## License

Choose a license before publishing this project publicly.
