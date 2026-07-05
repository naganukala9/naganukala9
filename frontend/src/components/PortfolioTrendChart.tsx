import { formatCompactCurrency, formatDate } from "../format";
import type { PortfolioHistoryPoint } from "../types";

interface Props {
  history: PortfolioHistoryPoint[];
}

const WIDTH = 960;
const HEIGHT = 160;
const PADDING = 24;

export function PortfolioTrendChart({ history }: Props) {
  if (history.length < 2) {
    return (
      <div className="card">
        <h2>Portfolio value over time</h2>
        <p className="empty-state">Upload more statements from different periods to see a trend line.</p>
      </div>
    );
  }

  const values = history.map((h) => h.total_portfolio_value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  const points = history.map((h, i) => {
    const x = PADDING + (i / (history.length - 1)) * (WIDTH - PADDING * 2);
    const y = HEIGHT - PADDING - ((h.total_portfolio_value - min) / range) * (HEIGHT - PADDING * 2);
    return { x, y, point: h };
  });

  const path = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");
  const last = points[points.length - 1];

  return (
    <div className="card">
      <h2>Portfolio value over time</h2>
      <svg className="trend-chart" viewBox={`0 0 ${WIDTH} ${HEIGHT}`} preserveAspectRatio="none">
        <line
          x1={PADDING}
          y1={HEIGHT - PADDING}
          x2={WIDTH - PADDING}
          y2={HEIGHT - PADDING}
          stroke="var(--baseline)"
          strokeWidth={1}
        />
        <path d={path} fill="none" stroke="var(--series-stock)" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
        {points.map(({ x, y, point }) => (
          <circle key={point.statement_id} cx={x} cy={y} r={4} fill="var(--series-stock)" stroke="var(--surface-1)" strokeWidth={2}>
            <title>
              {formatDate(point.as_of_date)}: {formatCompactCurrency(point.total_portfolio_value)}
            </title>
          </circle>
        ))}
        <text x={last.x} y={last.y - 12} textAnchor="end" fontSize={12} fill="var(--text-primary)">
          {formatCompactCurrency(last.point.total_portfolio_value)}
        </text>
      </svg>
    </div>
  );
}
