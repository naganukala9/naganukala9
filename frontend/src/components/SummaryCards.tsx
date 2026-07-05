import { formatCompactCurrency, formatDate } from "../format";
import type { Statement } from "../types";

interface Props {
  statement: Statement;
}

export function SummaryCards({ statement }: Props) {
  const total = statement.asset_allocation.find((r) => r.is_total);
  const changeInValue = total?.change_in_value ?? null;
  const changePositive = (changeInValue ?? 0) >= 0;
  const income = statement.retirement_income_estimate?.estimated_monthly_income ?? null;

  return (
    <div className="kpi-row">
      <div className="stat-tile">
        <div className="label">Total portfolio value</div>
        <div className="value">{formatCompactCurrency(statement.total_portfolio_value)}</div>
        <div className="label">as of {formatDate(statement.as_of_date)}</div>
      </div>

      {changeInValue !== null && (
        <div className="stat-tile">
          <div className="label">Change over period</div>
          <div className={`value delta ${changePositive ? "positive" : "negative"}`}>
            {changePositive ? "+" : ""}
            {formatCompactCurrency(changeInValue)}
          </div>
        </div>
      )}

      {income !== null && (
        <div className="stat-tile">
          <div className="label">Est. monthly retirement income</div>
          <div className="value">{formatCompactCurrency(income)}</div>
        </div>
      )}
    </div>
  );
}
