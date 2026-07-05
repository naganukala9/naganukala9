import { formatCurrency } from "../format";
import type { FundActivity } from "../types";

interface Props {
  rows: FundActivity[];
}

export function ActivitySummaryTable({ rows }: Props) {
  if (rows.length === 0) return null;

  return (
    <div className="card">
      <h2>Activity summary by fund</h2>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Fund</th>
              <th>Beginning value</th>
              <th>Additions</th>
              <th>Deductions</th>
              <th>Income</th>
              <th>Market fluctuation</th>
              <th>Ending value</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.label} className={row.is_total ? "total-row" : undefined}>
                <td>{row.label}</td>
                <td>{formatCurrency(row.beginning_value)}</td>
                <td>{formatCurrency(row.additions)}</td>
                <td>{formatCurrency(row.deductions)}</td>
                <td>{formatCurrency(row.income)}</td>
                <td>{formatCurrency(row.market_fluctuation)}</td>
                <td>{formatCurrency(row.ending_value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
