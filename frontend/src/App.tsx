import { useEffect, useState } from "react";
import { getPortfolioHistory, listStatements } from "./api";
import { ActivitySummaryTable } from "./components/ActivitySummaryTable";
import { AssetAllocationSection } from "./components/AssetAllocationSection";
import { BeneficiariesPanel } from "./components/BeneficiariesPanel";
import { InvestmentStyleTable } from "./components/InvestmentStyleTable";
import { PortfolioTrendChart } from "./components/PortfolioTrendChart";
import { RetirementEstimator } from "./components/RetirementEstimator";
import { StatementSelector } from "./components/StatementSelector";
import { SummaryCards } from "./components/SummaryCards";
import { UploadPanel } from "./components/UploadPanel";
import type { PortfolioHistoryPoint, Statement } from "./types";

export default function App() {
  const [statements, setStatements] = useState<Statement[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [history, setHistory] = useState<PortfolioHistoryPoint[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function refresh(preferredId?: string) {
    const [nextStatements, nextHistory] = await Promise.all([listStatements(), getPortfolioHistory()]);
    setStatements(nextStatements);
    setHistory(nextHistory);
    if (preferredId) {
      setSelectedId(preferredId);
    } else if (!selectedId && nextStatements.length > 0) {
      setSelectedId(nextStatements[0].id);
    }
  }

  useEffect(() => {
    refresh()
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load statements"))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const selected = statements.find((s) => s.id === selectedId) ?? null;

  return (
    <div className="app">
      <div className="app-header">
        <h1>Financial Statement Dashboard</h1>
        <StatementSelector statements={statements} selectedId={selectedId} onSelect={setSelectedId} />
      </div>

      {error && <div className="error-banner">{error}</div>}

      <UploadPanel
        onUploaded={(statement) => {
          setError(null);
          refresh(statement.id).catch((err) => setError(err instanceof Error ? err.message : "Failed to refresh"));
        }}
        onError={setError}
      />

      {loading ? (
        <p className="empty-state">Loading…</p>
      ) : selected ? (
        <>
          <SummaryCards statement={selected} />
          <PortfolioTrendChart history={history} />
          <AssetAllocationSection rows={selected.asset_allocation} />
          <InvestmentStyleTable rows={selected.investment_style} />
          <ActivitySummaryTable rows={selected.activity_summary} />
          <RetirementEstimator estimate={selected.retirement_income_estimate} />
          <BeneficiariesPanel groups={selected.beneficiaries} />
        </>
      ) : (
        <div className="card">
          <p className="empty-state">Upload a statement PDF to build your dashboard.</p>
        </div>
      )}
    </div>
  );
}
