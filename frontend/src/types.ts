export interface AssetAllocationRow {
  label: string;
  prior_value: number;
  prior_pct: number;
  current_value: number;
  current_pct: number;
  change_in_value: number;
  is_total: boolean;
}

export interface InvestmentStyleRow {
  label: string;
  money_market: number;
  bond_investment_grade: number;
  bond_high_yield: number;
  bond_international: number;
  stock_large_cap: number;
  stock_small_mid_cap: number;
  stock_international: number;
  stock_other: number;
  is_total: boolean;
}

export interface FundActivity {
  label: string;
  beginning_value: number;
  additions: number;
  deductions: number;
  income: number;
  market_fluctuation: number;
  ending_value: number;
  is_total: boolean;
}

export interface Beneficiary {
  name: string;
  tier: "primary" | "secondary";
  percentage: number;
}

export interface BeneficiaryGroup {
  fund_name: string | null;
  account_number: string | null;
  beneficiaries: Beneficiary[];
}

export interface RetirementScenario {
  additional_monthly_contribution: number;
  estimated_monthly_income: number;
}

export interface RetirementIncomeEstimate {
  current_balance: number | null;
  estimated_monthly_income: number | null;
  scenarios: RetirementScenario[];
}

export interface Statement {
  id: string;
  source_format: string;
  source_file: string;
  statement_period: string | null;
  as_of_date: string | null;
  investor_number: string | null;
  total_portfolio_value: number | null;
  asset_allocation: AssetAllocationRow[];
  investment_style: InvestmentStyleRow[];
  activity_summary: FundActivity[];
  beneficiaries: BeneficiaryGroup[];
  retirement_income_estimate: RetirementIncomeEstimate | null;
  extracted_at: string;
}

export interface PortfolioHistoryPoint {
  statement_id: string;
  as_of_date: string;
  total_portfolio_value: number;
}
