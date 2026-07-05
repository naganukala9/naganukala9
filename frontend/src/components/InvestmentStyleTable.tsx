import { formatPercent } from "../format";
import type { InvestmentStyleRow } from "../types";

interface Props {
  rows: InvestmentStyleRow[];
}

const COLUMNS: { key: keyof InvestmentStyleRow; label: string }[] = [
  { key: "money_market", label: "Money Market" },
  { key: "bond_investment_grade", label: "Bond: Inv. Grade" },
  { key: "bond_high_yield", label: "Bond: High Yield" },
  { key: "bond_international", label: "Bond: Int'l" },
  { key: "stock_large_cap", label: "Stock: Large-Cap" },
  { key: "stock_small_mid_cap", label: "Stock: Small/Mid" },
  { key: "stock_international", label: "Stock: Int'l" },
  { key: "stock_other", label: "Stock: Other" },
];

export function InvestmentStyleTable({ rows }: Props) {
  if (rows.length === 0) return null;

  return (
    <div className="card">
      <h2>Investment style analysis</h2>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Fund</th>
              {COLUMNS.map((c) => (
                <th key={c.key}>{c.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.label} className={row.is_total ? "total-row" : undefined}>
                <td>{row.label}</td>
                {COLUMNS.map((c) => (
                  <td key={c.key}>{formatPercent(row[c.key] as number)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
