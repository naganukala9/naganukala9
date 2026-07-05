from __future__ import annotations

import re
import uuid
from datetime import date, datetime

from app.models import (
    AssetAllocationRow,
    Beneficiary,
    BeneficiaryGroup,
    FundActivity,
    InvestmentStyleRow,
    RetirementIncomeEstimate,
    Statement,
)
from app.parsers.base import StatementParser, register
from app.parsers.row_parsing import rows_with_column_count

_INVESTMENT_STYLE_COLUMNS = [
    "money_market",
    "bond_investment_grade",
    "bond_high_yield",
    "bond_international",
    "stock_large_cap",
    "stock_small_mid_cap",
    "stock_international",
    "stock_other",
]

_TOTAL_LABELS = {"total portfolio", "total"}

_PERIOD_RE = re.compile(r"^([A-Za-z]+\s*-\s*[A-Za-z]+\s+\d{4})", re.MULTILINE)
_INVESTOR_NUMBER_RE = re.compile(r"Investor Number\s+(\d+)")
_PORTFOLIO_VALUE_RE = re.compile(
    r"As of (\d{2}/\d{2}/\d{2}) your total mutual fund portfolio value is \$([\d,]+\.\d{2})"
)
_CURRENT_BALANCE_RE = re.compile(r"Based on your current balance of \$([\d,]+\.\d{2})")
_ESTIMATED_INCOME_RE = re.compile(
    r"Your estimated monthly retirement income is\s*\$([\d,]+)"
)
_CONTRIBUTION_SCENARIO_RE = re.compile(
    r"Contributing an additional \$(\d+)/month\s*\$([\d,]+)"
)
_ACCOUNT_NUMBER_RE = re.compile(r"Account Number:\s*([\d\s\-]+\d)")
_PRIMARY_RE = re.compile(r"Primary:\s*(.+)")
_SECONDARY_RE = re.compile(r"Secondary:\s*(.+)")
_NAME_PCT_RE = re.compile(r"([A-Za-z][A-Za-z.'\-]*(?:\s+[A-Za-z][A-Za-z.'\-]*)*)\s+(\d+(?:\.\d+)?)%")


def _dollars(value: str) -> float:
    return float(value.replace(",", "").replace("$", ""))


def _is_total(label: str) -> bool:
    return label.strip().lower() in _TOTAL_LABELS


class TRowePriceParser(StatementParser):
    name = "trowe_price_portfolio_summary"

    def can_parse(self, pages: list[str]) -> bool:
        full_text = "\n".join(pages)
        return "T. Rowe Price" in full_text or "T Rowe Price" in full_text

    def parse(self, pages: list[str], source_file: str) -> Statement:
        full_text = "\n".join(pages)
        lines = [line for page in pages for line in page.splitlines()]

        statement_period = self._extract_statement_period(full_text)
        as_of_date, total_value = self._extract_portfolio_value(full_text)
        investor_number = self._extract_investor_number(full_text)

        asset_allocation = self._extract_asset_allocation(lines)
        investment_style = self._extract_investment_style(lines)
        activity_summary = self._extract_activity_summary(lines)
        beneficiaries = self._extract_beneficiaries(pages)
        retirement_estimate = self._extract_retirement_estimate(full_text)

        return Statement(
            id=str(uuid.uuid4()),
            source_format=self.name,
            source_file=source_file,
            statement_period=statement_period,
            as_of_date=as_of_date,
            investor_number=investor_number,
            total_portfolio_value=total_value,
            asset_allocation=asset_allocation,
            investment_style=investment_style,
            activity_summary=activity_summary,
            beneficiaries=beneficiaries,
            retirement_income_estimate=retirement_estimate,
            extracted_at=datetime.utcnow(),
        )

    @staticmethod
    def _extract_statement_period(full_text: str) -> str | None:
        match = _PERIOD_RE.search(full_text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _extract_investor_number(full_text: str) -> str | None:
        match = _INVESTOR_NUMBER_RE.search(full_text)
        return match.group(1) if match else None

    @staticmethod
    def _extract_portfolio_value(full_text: str) -> tuple[date | None, float | None]:
        match = _PORTFOLIO_VALUE_RE.search(full_text)
        if not match:
            return None, None
        as_of = datetime.strptime(match.group(1), "%m/%d/%y").date()
        return as_of, _dollars(match.group(2))

    @staticmethod
    def _extract_asset_allocation(lines: list[str]) -> list[AssetAllocationRow]:
        rows = rows_with_column_count(lines, 5)
        return [
            AssetAllocationRow(
                label=row.label,
                prior_value=row.values[0],
                prior_pct=row.values[1],
                current_value=row.values[2],
                current_pct=row.values[3],
                change_in_value=row.values[4],
                is_total=_is_total(row.label),
            )
            for row in rows
        ]

    @staticmethod
    def _extract_investment_style(lines: list[str]) -> list[InvestmentStyleRow]:
        rows = rows_with_column_count(lines, 7) + rows_with_column_count(lines, 8)
        result = []
        for row in rows:
            kwargs = dict(zip(_INVESTMENT_STYLE_COLUMNS, row.values))
            result.append(InvestmentStyleRow(label=row.label, is_total=_is_total(row.label), **kwargs))
        return result

    @staticmethod
    def _extract_activity_summary(lines: list[str]) -> list[FundActivity]:
        rows = rows_with_column_count(lines, 6)
        return [
            FundActivity(
                label=row.label,
                beginning_value=row.values[0],
                additions=row.values[1],
                deductions=row.values[2],
                income=row.values[3],
                market_fluctuation=row.values[4],
                ending_value=row.values[5],
                is_total=_is_total(row.label),
            )
            for row in rows
        ]

    @staticmethod
    def _extract_beneficiaries(pages: list[str]) -> list[BeneficiaryGroup]:
        # Beneficiary sections in these statements are laid out one account per
        # page, so we scan page-by-page rather than trying to detect paragraph
        # boundaries in the flattened text.
        groups: list[BeneficiaryGroup] = []
        for page in pages:
            account_match = _ACCOUNT_NUMBER_RE.search(page)
            primary_match = _PRIMARY_RE.search(page)
            secondary_match = _SECONDARY_RE.search(page)
            if not (primary_match or secondary_match):
                continue

            fund_name = None
            if account_match:
                pre_lines = page[: account_match.start()].strip().splitlines()
                if pre_lines:
                    fund_name = pre_lines[-1].strip()

            beneficiaries: list[Beneficiary] = []
            if primary_match:
                for name, pct in _NAME_PCT_RE.findall(primary_match.group(1)):
                    beneficiaries.append(Beneficiary(name=name.strip(), tier="primary", percentage=float(pct)))
            if secondary_match:
                for name, pct in _NAME_PCT_RE.findall(secondary_match.group(1)):
                    beneficiaries.append(Beneficiary(name=name.strip(), tier="secondary", percentage=float(pct)))

            if beneficiaries:
                groups.append(
                    BeneficiaryGroup(
                        fund_name=fund_name,
                        account_number=account_match.group(1).strip() if account_match else None,
                        beneficiaries=beneficiaries,
                    )
                )
        return groups

    @staticmethod
    def _extract_retirement_estimate(full_text: str) -> RetirementIncomeEstimate | None:
        balance_match = _CURRENT_BALANCE_RE.search(full_text)
        income_match = _ESTIMATED_INCOME_RE.search(full_text)
        scenarios = [
            {
                "additional_monthly_contribution": float(amount),
                "estimated_monthly_income": _dollars(income),
            }
            for amount, income in _CONTRIBUTION_SCENARIO_RE.findall(full_text)
        ]
        if not (balance_match or income_match or scenarios):
            return None
        return RetirementIncomeEstimate(
            current_balance=_dollars(balance_match.group(1)) if balance_match else None,
            estimated_monthly_income=_dollars(income_match.group(1)) if income_match else None,
            scenarios=scenarios,
        )


register(TRowePriceParser())
