"""Generic helpers for pulling labeled numeric rows out of flattened statement text.

Many brokerage/retirement statements render tables as PDF text where each row
collapses to a single line: a text label followed by a fixed number of numeric
columns (e.g. "Bond Funds $10,772.29 9.0% $16,439.26 11.0% $5,666.97"). Rather
than hardcoding label names, we detect rows by *how many* numeric tokens they
carry, which keeps this reusable across statement formats/layouts as long as
each table has a consistent column count.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_NUM_TOKEN = re.compile(r"-?\$?[\d,]+\.\d+%?|--")


@dataclass
class LabeledRow:
    label: str
    values: list[float]


def _parse_number(token: str) -> float:
    token = token.strip()
    if token == "--":
        return 0.0
    negative = token.startswith("-") and not token.startswith("--")
    token = token.lstrip("-").replace("$", "").replace(",", "").replace("%", "")
    value = float(token)
    return -value if negative else value


def parse_labeled_row(line: str) -> LabeledRow | None:
    """Split a line into its leading label and trailing numeric columns.

    Returns None if the line has no recognizable numeric columns.
    """
    match = _NUM_TOKEN.search(line)
    if not match:
        return None
    label = line[: match.start()].strip()
    if not label:
        return None
    tokens = _NUM_TOKEN.findall(line)
    values = [_parse_number(t) for t in tokens]
    return LabeledRow(label=label, values=values)


def rows_with_column_count(lines: list[str], count: int) -> list[LabeledRow]:
    """Return every labeled row in `lines` that has exactly `count` numeric columns."""
    rows = []
    for line in lines:
        row = parse_labeled_row(line)
        if row is not None and len(row.values) == count:
            rows.append(row)
    return rows


def rows_with_column_count_in(lines: list[str], counts: set[int]) -> list[LabeledRow]:
    rows = []
    for line in lines:
        row = parse_labeled_row(line)
        if row is not None and len(row.values) in counts:
            rows.append(row)
    return rows
