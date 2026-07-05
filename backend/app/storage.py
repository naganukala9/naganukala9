from __future__ import annotations

import json
from pathlib import Path

from app.models import Statement

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATEMENTS_DIR = DATA_DIR / "extracted"


def _ensure_dirs() -> None:
    STATEMENTS_DIR.mkdir(parents=True, exist_ok=True)


def save_statement(statement: Statement) -> Path:
    _ensure_dirs()
    path = STATEMENTS_DIR / f"{statement.id}.json"
    path.write_text(statement.model_dump_json(indent=2))
    return path


def load_statement(statement_id: str) -> Statement | None:
    path = STATEMENTS_DIR / f"{statement_id}.json"
    if not path.exists():
        return None
    return Statement.model_validate_json(path.read_text())


def list_statements() -> list[Statement]:
    _ensure_dirs()
    statements = [Statement.model_validate_json(p.read_text()) for p in STATEMENTS_DIR.glob("*.json")]
    statements.sort(key=lambda s: s.extracted_at, reverse=True)
    return statements


def delete_statement(statement_id: str) -> bool:
    path = STATEMENTS_DIR / f"{statement_id}.json"
    if not path.exists():
        return False
    path.unlink()
    return True
