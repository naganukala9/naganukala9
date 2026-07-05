import type { PortfolioHistoryPoint, Statement } from "./types";

const BASE = "/api";

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function uploadStatement(file: File): Promise<Statement> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/statements/upload`, { method: "POST", body: form });
  return asJson<Statement>(res);
}

export async function listStatements(): Promise<Statement[]> {
  const res = await fetch(`${BASE}/statements`);
  return asJson<Statement[]>(res);
}

export async function getStatement(id: string): Promise<Statement> {
  const res = await fetch(`${BASE}/statements/${id}`);
  return asJson<Statement>(res);
}

export async function deleteStatement(id: string): Promise<void> {
  const res = await fetch(`${BASE}/statements/${id}`, { method: "DELETE" });
  await asJson(res);
}

export async function getPortfolioHistory(): Promise<PortfolioHistoryPoint[]> {
  const res = await fetch(`${BASE}/dashboard/portfolio-history`);
  return asJson<PortfolioHistoryPoint[]>(res);
}
