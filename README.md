# SmartDoc AI — Hybrid RAG with Reranking

A full-stack AI-powered PDF search application that combines keyword retrieval, semantic search, hybrid ranking, and cross-encoder reranking to find relevant passages in documents.

**Built with:** Python · FastAPI · React · TypeScript · Sentence Transformers · BM25

## Overview

SmartDoc AI lets users upload a PDF and search its contents through a web interface. It extracts document text, splits it into chunks, retrieves candidates using keyword and semantic search, combines their rankings using Reciprocal Rank Fusion (RRF), and reranks the candidates using a cross-encoder model.

The goal is to explore practical document retrieval techniques used in Retrieval-Augmented Generation (RAG) systems.

## Features

- **PDF text extraction:** Extract text while preserving page numbers.
- **Text chunking:** Split extracted text into overlapping chunks.
- **BM25 keyword search:** Retrieve passages based on matching terms.
- **Semantic search:** Represent text as embeddings using Sentence Transformers.
- **Hybrid retrieval:** Combine keyword and semantic rankings with Reciprocal Rank Fusion.
- **Cross-encoder reranking:** Reorder retrieved passages based on query-document relevance.
- **REST API:** Upload PDFs and search indexed content through FastAPI.
- **Interactive frontend:** React and TypeScript interface for document upload and search.
- **Automated tests:** Tests for API behavior, keyword retrieval, semantic retrieval, hybrid search, and reranking.

## Architecture

The retrieval pipeline follows these stages:

1. The user uploads a PDF through the frontend.
2. FastAPI validates the upload and extracts text using PyMuPDF.
3. The extracted text is split into overlapping chunks.
4. BM25 retrieves keyword-based candidates.
5. Sentence Transformers embeddings support semantic retrieval.
6. Reciprocal Rank Fusion combines the two rankings.
7. A cross-encoder reranks the candidate passages.
8. The API returns ranked results with chunk and page metadata.

### Architecture Diagram

See the [detailed architecture documentation](docs/architecture.md) for the pipeline and component descriptions.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, CSS |
| Backend API | Python, FastAPI, Uvicorn |
| PDF processing | PyMuPDF |
| Keyword retrieval | BM25 via `rank-bm25` |
| Semantic retrieval | Sentence Transformers |
| Hybrid ranking | Reciprocal Rank Fusion |
| Reranking | Cross-Encoder |
| Numerical operations | NumPy |
| Testing | Pytest, HTTPX |
| Version control | Git, GitHub |

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
│   ├── src/
│   ├── package.json
│   └── ...
├── tests/
│   ├── test_api.py
│   ├── test_keyword_search.py
│   ├── test_semantic_search.py
│   ├── test_hybrid_search.py
│   └── test_reranker.py
├── docs/
│   └── architecture.md
├── sample_data/
├── .gitignore
└── README.md
```

## Prerequisites

Install the following before running the application:

- Python 3.12 recommended
- Node.js and npm
- Git
- Internet connection for the initial download of the machine-learning models

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Sandeepkumar004-hub/SmartDoc-AI.git
cd SmartDoc-AI
```

### 2. Create and activate a Python virtual environment

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

From the project root, run:

```powershell
python -m pip install fastapi "uvicorn[standard]" python-multipart pymupdf rank-bm25 sentence-transformers numpy pytest httpx
```

### 4. Start the backend

```powershell
python -m uvicorn backend.main:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

Health check: `http://127.0.0.1:8000/health`

### 5. Install and start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local frontend URL printed in the terminal, usually `http://localhost:5173/`.

### 6. Use the application

1. Open the frontend in your browser.
2. Select a PDF file and upload it.
3. Enter a question or keywords related to the document.
4. Review the ranked passages and their page numbers.

The first upload may take longer while the embedding and reranking models initialize or download.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Check backend health |
| POST | `/upload` | Upload and index a PDF |
| POST | `/search` | Retrieve and rerank document passages |

### Example Search Request

```json
{
  "query": "frontend web application development",
  "top_k": 5
}
```

### Search Result Fields

Search responses include:

- `query`: submitted search query
- `filename`: currently indexed PDF filename
- `retrieval_method`: retrieval pipeline identifier
- `result_count`: number of returned passages
- `results`: ranked document chunks, including text, page and chunk identifiers, RRF score, and reranker score

The `score` field represents the final reranker score. `rrf_score` preserves the hybrid retrieval score, and `rerank_score` contains the cross-encoder score.

## Run Tests

Activate the virtual environment and run the complete test suite from the project root:

```powershell
python -m pytest -v
```

**Current development status:** 34 automated tests passed in the local development environment.

## Current Limitations

- The application supports one active PDF index at a time.
- The document index is stored in memory and is cleared when the backend restarts.
- Scanned PDFs without extractable text may require OCR.
- The first model initialization requires internet access to download the models.
- Retrieval quality depends on document content, chunking, query wording, and model behavior.
- The project has been tested locally; production deployment and security hardening remain future work.

## Future Improvements

- Support multiple PDFs and persistent document indexes.
- Add OCR for scanned documents.
- Add source citations and highlighted matching passages.
- Evaluate retrieval quality using a labeled query dataset and ranking metrics.
- Add authentication and access controls.
- Deploy the frontend and backend for a public live demo.
- Add monitoring and performance evaluation.

## Author

**Sandeep Kumar**

- GitHub: [Sandeepkumar004-hub](https://github.com/Sandeepkumar004-hub)
- Project repository: [SmartDoc AI](https://github.com/Sandeepkumar004-hub/SmartDoc-AI)

---

*SmartDoc AI is a learning and portfolio project exploring PDF processing, semantic retrieval, hybrid search, and cross-encoder reranking.*