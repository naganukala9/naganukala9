import type { Statement } from "../types";

interface Props {
  statements: Statement[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function StatementSelector({ statements, selectedId, onSelect }: Props) {
  if (statements.length === 0) return null;

  return (
    <select className="select" value={selectedId ?? ""} onChange={(e) => onSelect(e.target.value)}>
      {statements.map((s) => (
        <option key={s.id} value={s.id}>
          {s.statement_period ?? s.source_file} — {s.as_of_date ?? "undated"}
        </option>
      ))}
    </select>
  );
}
