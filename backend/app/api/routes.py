from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app import storage
from app.models import Statement
from app.parsers import find_parser
from app.pdf_reader import read_pdf_pages

router = APIRouter()


@router.post("/statements/upload", response_model=Statement)
async def upload_statement(file: UploadFile) -> Statement:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp.flush()
        pages = read_pdf_pages(tmp.name)

    parser = find_parser(pages)
    if parser is None:
        raise HTTPException(status_code=422, detail="No parser recognizes this statement format")

    statement = parser.parse(pages, source_file=file.filename)
    storage.save_statement(statement)
    return statement


@router.get("/statements", response_model=list[Statement])
def list_statements() -> list[Statement]:
    return storage.list_statements()


@router.get("/statements/{statement_id}", response_model=Statement)
def get_statement(statement_id: str) -> Statement:
    statement = storage.load_statement(statement_id)
    if statement is None:
        raise HTTPException(status_code=404, detail="Statement not found")
    return statement


@router.delete("/statements/{statement_id}")
def delete_statement(statement_id: str) -> dict:
    if not storage.delete_statement(statement_id):
        raise HTTPException(status_code=404, detail="Statement not found")
    return {"deleted": statement_id}


@router.get("/dashboard/portfolio-history")
def portfolio_history() -> list[dict]:
    history = [
        {
            "statement_id": s.id,
            "as_of_date": s.as_of_date,
            "total_portfolio_value": s.total_portfolio_value,
        }
        for s in storage.list_statements()
        if s.as_of_date is not None
    ]
    history.sort(key=lambda h: h["as_of_date"])
    return history


@router.get("/dashboard/latest", response_model=Statement)
def latest_statement() -> Statement:
    statements = storage.list_statements()
    if not statements:
        raise HTTPException(status_code=404, detail="No statements have been uploaded yet")
    return statements[0]
