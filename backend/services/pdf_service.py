import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text content from a PDF file."""
    doc = fitz.open(pdf_path)
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts)


def get_page_count(pdf_path: str) -> int:
    """Return the number of pages in a PDF."""
    doc = fitz.open(pdf_path)
    count = doc.page_count
    doc.close()
    return count


def extract_text_chunked(pdf_path: str, max_chars: int = 15000) -> str:
    """Extract text up to max_chars — used to stay within LLM context windows."""
    full_text = extract_text_from_pdf(pdf_path)
    return full_text[:max_chars]
