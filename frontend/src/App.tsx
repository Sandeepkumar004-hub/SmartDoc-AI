
import { useState } from "react";
import "./App.css";

type SearchResult = {
  chunk_id: number;
  page_number: number;
  text: string;
  score: number;
};

type UploadResponse = {
  filename: string;
  page_count: number;
  chunk_count: number;
  message: string;
};

type SearchResponse = {
  query: string;
  filename: string | null;
  result_count: number;
  results: SearchResult[];
};

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [filename, setFilename] = useState("");
  const [pageCount, setPageCount] = useState(0);
  const [chunkCount, setChunkCount] = useState(0);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [uploaded, setUploaded] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function handleUpload() {
    if (!file) {
      setError("Please select a PDF file first.");
      return;
    }

    setUploading(true);
    setError("");
    setMessage("");
    setResults([]);
    setUploaded(false);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "PDF upload failed.");
      }

      setFilename(data.filename);
      setPageCount(data.page_count);
      setChunkCount(data.chunk_count);
      setUploaded(true);
      setMessage(data.message || "PDF uploaded and indexed successfully.");
    } catch (err) {
      setError(
        err instanceof Error
          ? `${err.message} Check that the backend is running.`
          : "Something went wrong during upload.",
      );
    } finally {
      setUploading(false);
    }
  }

  async function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!uploaded) {
      setError("Upload a PDF before searching.");
      return;
    }

    if (!query.trim()) {
      setError("Please enter a search query.");
      return;
    }

    setSearching(true);
    setError("");
    setMessage("");
    setResults([]);

    try {
      const response = await fetch(`${API_URL}/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query.trim(),
          top_k: 5,
        }),
      });

      const data: SearchResponse & { detail?: string } =
        await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Search failed.");
      }

      setResults(data.results);
      setMessage(
        data.result_count > 0
          ? `Found ${data.result_count} matching result(s).`
          : "No matching text found. Try different keywords.",
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? `${err.message} Check that the backend is running.`
          : "Something went wrong during search.",
      );
    } finally {
      setSearching(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/">
          <span className="brand-icon">S</span>
          <span>SmartDoc <strong>AI</strong></span>
        </a>
        <span className="status-pill">
          <span className="status-dot" />
          Document Search
        </span>
      </header>

      <section className="hero">
        <div className="eyebrow">YOUR DOCUMENT, UNDERSTOOD</div>
        <h1>
          Find answers in your
          <span> documents.</span>
        </h1>
        <p>
          Upload a PDF and search its contents with intelligent,
          ranked keyword retrieval.
        </p>
      </section>

      <section className="workspace">
        <div className="panel upload-panel">
          <div className="panel-heading">
            <span className="step-number">01</span>
            <div>
              <h2>Upload document</h2>
              <p>Select a PDF to get started.</p>
            </div>
          </div>

          <label className="dropzone">
            <span className="upload-icon">↑</span>
            <strong>{file ? file.name : "Choose a PDF file"}</strong>
            <span>
              {file
                ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
                : "PDF format · Maximum 10 MB"}
            </span>
            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                const selectedFile = event.target.files?.[0] ?? null;
                setFile(selectedFile);
                setError("");
                setMessage("");
              }}
            />
          </label>

          <button
            className="primary-button"
            onClick={handleUpload}
            disabled={uploading || !file}
          >
            {uploading ? "Processing PDF..." : "Upload and index PDF"}
          </button>

          {uploaded && (
            <div className="document-summary">
              <div className="document-name">
                <span className="pdf-badge">PDF</span>
                <div>
                  <strong>{filename}</strong>
                  <span>Indexed and ready to search</span>
                </div>
              </div>
              <div className="document-stats">
                <div>
                  <strong>{pageCount}</strong>
                  <span>Pages</span>
                </div>
                <div>
                  <strong>{chunkCount}</strong>
                  <span>Chunks</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="panel search-panel">
          <div className="panel-heading">
            <span className="step-number">02</span>
            <div>
              <h2>Search document</h2>
              <p>What would you like to find?</p>
            </div>
          </div>

          <form onSubmit={handleSearch}>
            <label className="input-label" htmlFor="query">
              YOUR QUESTION OR KEYWORDS
            </label>
            <textarea
              id="query"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="e.g. What technical projects are mentioned?"
              rows={4}
              maxLength={500}
            />
            <div className="input-footer">
              <span>{query.length}/500 characters</span>
              <span>Up to 5 results</span>
            </div>
            <button
              className="primary-button"
              type="submit"
              disabled={searching || !uploaded}
            >
              {searching ? "Searching..." : "Search document →"}
            </button>
          </form>

          {!uploaded && (
            <p className="helper-text">
              Upload a PDF first to enable document search.
            </p>
          )}
        </div>
      </section>

      {(error || message) && (
        <div
          className={`notice ${error ? "notice-error" : "notice-success"}`}
          role="status"
        >
          {error || message}
        </div>
      )}

      <section className="results-section">
        <div className="results-heading">
          <div>
            <div className="eyebrow">RETRIEVAL OUTPUT</div>
            <h2>Search results</h2>
          </div>
          <span className="result-count">
            {results.length} result{results.length === 1 ? "" : "s"}
          </span>
        </div>

        {results.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">⌕</span>
            <strong>Your results will appear here</strong>
            <p>Upload a document and search for a topic or keyword.</p>
          </div>
        ) : (
          <div className="results-list">
            {results.map((result) => (
              <article className="result-card" key={result.chunk_id}>
                <div className="result-meta">
                  <span>CHUNK {result.chunk_id}</span>
                  <span>PAGE {result.page_number}</span>
                  <span>SCORE {result.score.toFixed(4)}</span>
                </div>
                <p>{result.text}</p>
              </article>
            ))}
          </div>
        )}
      </section>

      <footer className="footer">
        <span>SmartDoc AI</span>
        <span>FastAPI · BM25 Retrieval · React + TypeScript</span>
      </footer>
    </main>
  );
}

export default App;
