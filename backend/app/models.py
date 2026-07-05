from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class AssetAllocationRow(BaseModel):
    label: str
    prior_value: float
    prior_pct: float
    current_value: float
    current_pct: float
    change_in_value: float
    is_total: bool = False


class InvestmentStyleRow(BaseModel):
    label: str
    money_market: float = 0.0
    bond_investment_grade: float = 0.0
    bond_high_yield: float = 0.0
    bond_international: float = 0.0
    stock_large_cap: float = 0.0
    stock_small_mid_cap: float = 0.0
    stock_international: float = 0.0
    stock_other: float = 0.0
    is_total: bool = False


class FundActivity(BaseModel):
    label: str
    beginning_value: float
    additions: float
    deductions: float
    income: float
    market_fluctuation: float
    ending_value: float
    is_total: bool = False


class Beneficiary(BaseModel):
    name: str
    tier: str  # "primary" | "secondary"
    percentage: float


class BeneficiaryGroup(BaseModel):
    fund_name: Optional[str] = None
    account_number: Optional[str] = None
    beneficiaries: list[Beneficiary] = Field(default_factory=list)


class RetirementIncomeEstimate(BaseModel):
    current_balance: Optional[float] = None
    estimated_monthly_income: Optional[float] = None
    scenarios: list[dict] = Field(default_factory=list)  # [{additional_monthly_contribution, estimated_monthly_income}]


class Statement(BaseModel):
    id: str
    source_format: str
    source_file: str
    statement_period: Optional[str] = None
    as_of_date: Optional[date] = None
    investor_number: Optional[str] = None
    total_portfolio_value: Optional[float] = None
    asset_allocation: list[AssetAllocationRow] = Field(default_factory=list)
    investment_style: list[InvestmentStyleRow] = Field(default_factory=list)
    activity_summary: list[FundActivity] = Field(default_factory=list)
    beneficiaries: list[BeneficiaryGroup] = Field(default_factory=list)
    retirement_income_estimate: Optional[RetirementIncomeEstimate] = None
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
