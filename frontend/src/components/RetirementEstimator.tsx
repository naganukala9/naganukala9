import { formatCurrency } from "../format";
import type { RetirementIncomeEstimate } from "../types";

interface Props {
  estimate: RetirementIncomeEstimate | null;
}

export function RetirementEstimator({ estimate }: Props) {
  if (!estimate) return null;

  return (
    <div className="card">
      <h2>Retirement monthly income estimator</h2>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Scenario</th>
              <th>Estimated monthly income</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Current balance ({formatCurrency(estimate.current_balance)})</td>
              <td>{formatCurrency(estimate.estimated_monthly_income)}</td>
            </tr>
            {estimate.scenarios.map((s) => (
              <tr key={s.additional_monthly_contribution}>
                <td>+ {formatCurrency(s.additional_monthly_contribution)}/month contribution</td>
                <td>{formatCurrency(s.estimated_monthly_income)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
