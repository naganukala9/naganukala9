from __future__ import annotations

from pathlib import Path

import pdfplumber


def read_pdf_pages(path: str | Path) -> list[str]:
    """Return each page's extracted text, in page order."""
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages
