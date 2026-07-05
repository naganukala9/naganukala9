import { formatPercent } from "../format";
import type { BeneficiaryGroup } from "../types";

interface Props {
  groups: BeneficiaryGroup[];
}

export function BeneficiariesPanel({ groups }: Props) {
  if (groups.length === 0) return null;

  return (
    <div className="card">
      <h2>Beneficiaries</h2>
      {groups.map((group, i) => (
        <div className="beneficiary-group" key={group.account_number ?? i}>
          <h3>
            {group.fund_name ?? "Account"}
            {group.account_number ? ` — ${group.account_number}` : ""}
          </h3>
          <div className="beneficiary-list">
            {group.beneficiaries.map((b, j) => (
              <div key={j}>
                <span className="beneficiary-tier">{b.tier}</span>
                {b.name} ({formatPercent(b.percentage)})
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
