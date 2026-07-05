import datetime

from app.parsers.trowe_price import TRowePriceParser
from tests.fixtures.trowe_price_sample_pages import get_sample_pages


def _parsed():
    parser = TRowePriceParser()
    pages = get_sample_pages()
    assert parser.can_parse(pages)
    return parser.parse(pages, source_file="fake_statement.pdf")


def test_extracts_header_fields():
    statement = _parsed()
    assert statement.source_format == "trowe_price_portfolio_summary"
    assert statement.statement_period == "January - December 2024"
    assert statement.investor_number == "999999999"
    assert statement.as_of_date == datetime.date(2024, 12, 31)
    assert statement.total_portfolio_value == 200000.00


def test_extracts_asset_allocation_rows():
    statement = _parsed()
    by_label = {row.label: row for row in statement.asset_allocation}
    assert by_label["Money Market Funds"].current_value == 7000.00
    assert by_label["Money Market Funds"].current_pct == 3.0
    assert by_label["Bond Funds"].change_in_value == 4000.00
    assert by_label["Total Portfolio"].is_total is True
    assert by_label["Tax - Free"].current_value == 0.0


def test_extracts_investment_style_rows():
    statement = _parsed()
    fund_row = next(r for r in statement.investment_style if r.label == "Retirement 2045")
    assert fund_row.stock_large_cap == 38.0
    assert fund_row.stock_other == 0.0  # not present in the 7-column fund row

    total_row = next(r for r in statement.investment_style if r.is_total)
    assert total_row.stock_other == 0.0


def test_extracts_activity_summary():
    statement = _parsed()
    fund_activity = next(a for a in statement.activity_summary if a.label == "Retirement 2045")
    assert fund_activity.beginning_value == 180000.00
    assert fund_activity.income == 5000.00
    assert fund_activity.market_fluctuation == 15000.00
    assert fund_activity.ending_value == 200000.00


def test_extracts_beneficiaries():
    statement = _parsed()
    assert len(statement.beneficiaries) == 1
    group = statement.beneficiaries[0]
    assert group.account_number == "1234567890 - 1"
    names_by_tier = {(b.tier, b.name): b.percentage for b in group.beneficiaries}
    assert names_by_tier[("primary", "John Q Sample")] == 100.0
    assert names_by_tier[("secondary", "Alex R Sample")] == 50.0
    assert names_by_tier[("secondary", "Casey T Sample")] == 50.0


def test_extracts_retirement_income_estimate():
    statement = _parsed()
    estimate = statement.retirement_income_estimate
    assert estimate is not None
    assert estimate.current_balance == 200000.00
    assert estimate.estimated_monthly_income == 1750.0
    assert {"additional_monthly_contribution": 150.0, "estimated_monthly_income": 1900.0} in estimate.scenarios
    assert {"additional_monthly_contribution": 300.0, "estimated_monthly_income": 2050.0} in estimate.scenarios
