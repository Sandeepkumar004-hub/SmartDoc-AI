
def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """Split extracted PDF pages into overlapping text chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    chunk_id = 1
    step = chunk_size - overlap

    for page in pages:
        text = page["text"].strip()

        if not text:
            continue

        for start in range(0, len(text), step):
            chunk_text = text[start:start + chunk_size].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_number": page["page_number"],
                    "text": chunk_text,
                })
                chunk_id += 1

    return chunks
