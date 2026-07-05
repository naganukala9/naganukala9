from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import Statement

_REGISTRY: list["StatementParser"] = []


class StatementParser(ABC):
    """Base interface every statement-format parser implements.

    Add a new statement format (Fidelity, Vanguard, a bank statement, ...) by
    subclassing this, implementing `can_parse` / `parse`, and registering an
    instance in `app/parsers/__init__.py`. `find_parser` picks the first
    registered parser that claims the document.
    """

    name: str

    @abstractmethod
    def can_parse(self, pages: list[str]) -> bool:
        ...

    @abstractmethod
    def parse(self, pages: list[str], source_file: str) -> Statement:
        ...


def register(parser: StatementParser) -> StatementParser:
    _REGISTRY.append(parser)
    return parser


def find_parser(pages: list[str]) -> StatementParser | None:
    for parser in _REGISTRY:
        if parser.can_parse(pages):
            return parser
    return None


def registered_parsers() -> list[StatementParser]:
    return list(_REGISTRY)
