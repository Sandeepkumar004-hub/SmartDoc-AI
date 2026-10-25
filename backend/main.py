
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.chunker import chunk_pages
from backend.keyword_search import KeywordSearch
from backend.pdf_processor import extract_pdf_pages

app = FastAPI(
    title="SmartDoc AI",
    description="Hybrid RAG with Reranking",
    version="0.3.0",
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# In-memory keyword index for the currently uploaded PDF
keyword_search = KeywordSearch()
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
    global keyword_search, current_filename

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

    temp_path = None

    try:
        with NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            temp.write(content)
            temp_path = temp.name

        # Extract text and page numbers
        pages = extract_pdf_pages(temp_path)

        if not pages:
            raise HTTPException(
                status_code=422,
                detail="No extractable text found in this PDF.",
            )

        # Split extracted text into chunks
        chunks = chunk_pages(pages)

        if not chunks:
            raise HTTPException(
                status_code=422,
                detail="Could not create text chunks from this PDF.",
            )

        # Build a new index before replacing the current one
        new_search = KeywordSearch()
        new_search.build_index(chunks)

        keyword_search = new_search
        current_filename = Path(file.filename).name

        return {
            "filename": current_filename,
            "page_count": len(pages),
            "chunk_count": len(chunks),
            "message": "PDF processed and indexed successfully.",
            "chunks": chunks,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Could not process this PDF. Try another PDF.",
        )

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)

        await file.close()


@app.post("/search")
def search_documents(request: SearchRequest):
    if keyword_search.index is None:
        raise HTTPException(
            status_code=400,
            detail="Upload a PDF before searching.",
        )

    results = keyword_search.search(
        request.query,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "filename": current_filename,
        "result_count": len(results),
        "results": results,
    }
