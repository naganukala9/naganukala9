from app.parsers.row_parsing import parse_labeled_row, rows_with_column_count


def test_parses_dollar_and_percent_row():
    row = parse_labeled_row("Money Market Funds $6,000.00 3.0% $7,000.00 3.0% $1,000.00")
    assert row.label == "Money Market Funds"
    assert row.values == [6000.00, 3.0, 7000.00, 3.0, 1000.00]


def test_treats_double_dash_as_zero():
    row = parse_labeled_row("Tax - Free -- -- -- -- --")
    assert row.label == "Tax - Free"
    assert row.values == [0.0, 0.0, 0.0, 0.0, 0.0]


def test_handles_negative_values():
    row = parse_labeled_row("Stock Funds $176,000.00 88.0% $171,000.00 86.0% -5,000.00")
    assert row.values[-1] == -5000.00


def test_ignores_lines_without_numbers():
    assert parse_labeled_row("Portfolio Summary") is None


def test_ignores_lines_without_a_label():
    assert parse_labeled_row("$1,234.56") is None


def test_filters_by_column_count():
    lines = [
        "Money Market Funds $6,000.00 3.0% $7,000.00 3.0% $1,000.00",
        "Retirement 2045 $180,000.00 $0.00 $0.00 $5,000.00 $15,000.00 $200,000.00",
    ]
    five_col_rows = rows_with_column_count(lines, 5)
    six_col_rows = rows_with_column_count(lines, 6)
    assert [r.label for r in five_col_rows] == ["Money Market Funds"]
    assert [r.label for r in six_col_rows] == ["Retirement 2045"]
