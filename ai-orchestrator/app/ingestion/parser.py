from typing import Tuple, List
import pdfplumber
import re
import io


def clean_text(text: str) -> str:
    """
    Normalize whitespace and remove obvious artifacts.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_pdf(file_bytes: bytes) -> Tuple[str, List[str]]:
    """
    Extract text from a PDF.

    Returns:
        full_text: str
        page_texts: List[str] (per-page text, useful for metadata later)
    """
    full_text_parts = []
    page_texts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            page_text = clean_text(page_text)

            if page_text:
                page_texts.append(page_text)
                full_text_parts.append(page_text)

    full_text = "\n".join(full_text_parts)
    return full_text, page_texts


def parse_document(file_bytes: bytes, filename: str) -> dict:
    """
    Entry point parser. Returns a standard structure regardless of file type.
    """
    if filename.lower().endswith(".pdf"):
        full_text, pages = parse_pdf(file_bytes)
    else:
        raise ValueError(f"Unsupported document type: {filename}")

    return {
        "full_text": full_text,
        "pages": pages,
        "char_count": len(full_text)
    }