import { formatCurrency, formatPercent } from "../format";
import type { AssetAllocationRow } from "../types";

interface Props {
  rows: AssetAllocationRow[];
}

const TOP_LEVEL_CATEGORIES: { label: string; series: string; cssVar: string }[] = [
  { label: "Stock Funds", series: "Stock", cssVar: "--series-stock" },
  { label: "Bond Funds", series: "Bond", cssVar: "--series-bond" },
  { label: "Money Market Funds", series: "Money Market", cssVar: "--series-money-market" },
];

export function AssetAllocationSection({ rows }: Props) {
  const byLabel = new Map(rows.map((r) => [r.label.trim().toLowerCase(), r]));
  const segments = TOP_LEVEL_CATEGORIES.map((cat) => ({
    ...cat,
    row: byLabel.get(cat.label.toLowerCase()),
  })).filter((s) => s.row && s.row.current_value > 0);

  const total = segments.reduce((sum, s) => sum + (s.row?.current_value ?? 0), 0);

  return (
    <div className="card">
      <h2>Asset allocation</h2>
      {segments.length === 0 ? (
        <p className="empty-state">No asset allocation data extracted for this statement.</p>
      ) : (
        <>
          <div className="stacked-bar-legend">
            {segments.map((s) => (
              <span key={s.label} className="legend-item">
                <span className="legend-swatch" style={{ background: `var(${s.cssVar})` }} />
                {s.series} — {formatPercent(s.row!.current_pct)}
              </span>
            ))}
          </div>
          <div className="stacked-bar">
            {segments.map((s) => {
              const widthPct = total > 0 ? (s.row!.current_value / total) * 100 : 0;
              return (
                <div
                  key={s.label}
                  className="stacked-bar-segment"
                  style={{ width: `${widthPct}%`, background: `var(${s.cssVar})` }}
                  title={`${s.series}: ${formatCurrency(s.row!.current_value)} (${formatPercent(s.row!.current_pct)})`}
                >
                  {widthPct > 12 ? formatPercent(s.row!.current_pct) : ""}
                </div>
              );
            })}
          </div>
        </>
      )}

      <div className="table-scroll" style={{ marginTop: 20 }}>
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Prior value</th>
              <th>Prior %</th>
              <th>Current value</th>
              <th>Current %</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.label} className={row.is_total ? "total-row" : undefined}>
                <td>{row.label}</td>
                <td>{formatCurrency(row.prior_value)}</td>
                <td>{formatPercent(row.prior_pct)}</td>
                <td>{formatCurrency(row.current_value)}</td>
                <td>{formatPercent(row.current_pct)}</td>
                <td className={row.change_in_value >= 0 ? "delta positive" : "delta negative"}>
                  {row.change_in_value >= 0 ? "+" : ""}
                  {formatCurrency(row.change_in_value)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
