from backend.keyword_search import KeywordSearch
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.chunker import chunk_pages
from backend.hybrid_search import HybridSearch
from backend.pdf_processor import extract_pdf_pages


app = FastAPI(
    title="SmartDoc AI",
    description="PDF search using hybrid BM25 and semantic retrieval",
    version="0.5.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# The hybrid index is built when a PDF is uploaded.
hybrid_search = None
current_filename = None


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=10)


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartDoc AI!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global hybrid_search, current_filename

    temp_path = None

    try:
        if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=400,
                detail="Please upload a PDF file.",
            )

        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF must be 10 MB or smaller.",
            )

        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF.",
            )

        with NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp:
            temp.write(content)
            temp_path = temp.name

        pages = extract_pdf_pages(temp_path)

        if not pages:
            raise HTTPException(
                status_code=422,
                detail="No extractable text found in this PDF.",
            )

        chunks = chunk_pages(pages)

        if not chunks:
            raise HTTPException(
                status_code=422,
                detail="Could not create text chunks from this PDF.",
            )

        # Build the new index before replacing the current one.
        new_search = HybridSearch()
        new_search.build_index(chunks)

        hybrid_search = new_search
        current_filename = Path(file.filename).name

        return {
            "filename": current_filename,
            "page_count": len(pages),
            "chunk_count": len(chunks),
            "message": "PDF processed and hybrid index built successfully.",
            "retrieval_method": "hybrid_bm25_semantic_rrf",
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Could not process this PDF or build its search index.",
        )

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
        await file.close()


@app.post("/search")
def search_documents(request: SearchRequest):
    if hybrid_search is None:
        raise HTTPException(
            status_code=400,
            detail="Upload a PDF before searching.",
        )

    results = hybrid_search.search(
        request.query,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "filename": current_filename,
        "retrieval_method": "hybrid_bm25_semantic_rrf",
        "result_count": len(results),
        "results": results,
    }
