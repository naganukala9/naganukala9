import { useState } from "react";
import { uploadStatement } from "../api";
import type { Statement } from "../types";

interface Props {
  onUploaded: (statement: Statement) => void;
  onError: (message: string) => void;
}

export function UploadPanel({ onUploaded, onError }: Props) {
  const [busy, setBusy] = useState(false);

  async function handleFile(file: File | undefined, input: HTMLInputElement) {
    if (!file) return;
    setBusy(true);
    try {
      const statement = await uploadStatement(file);
      onUploaded(statement);
    } catch (err) {
      onError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setBusy(false);
      input.value = "";
    }
  }

  return (
    <div className="card">
      <h2>Add a statement</h2>
      <div className="upload-panel">
        <input
          type="file"
          accept="application/pdf"
          disabled={busy}
          onChange={(e) => handleFile(e.target.files?.[0], e.target)}
        />
        {busy && <span className="empty-state">Extracting…</span>}
      </div>
    </div>
  );
}
