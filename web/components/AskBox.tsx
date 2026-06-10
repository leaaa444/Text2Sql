"use client";

import { useState } from "react";
import { ask, type AskResult } from "@/lib/api";
import DataTable from "@/components/DataTable";

export default function AskBox() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AskResult | null>(null);

  async function onAsk() {
    const q = question.trim();
    if (!q) return;
    setLoading(true);
    setResult(null);
    try {
      setResult(await ask(q));
    } catch {
      setResult({ error: "Backend nije dostupan (proveri da li je server pokrenut)." });
    }
    setLoading(false);
  }

  return (
    <div className="card">
      <h2>Postavi pitanje (prirodni jezik → SQL)</h2>
      <div className="row">
        <input
          type="text"
          value={question}
          placeholder="npr. Koja tri proizvoda su najskuplja?"
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") onAsk();
          }}
        />
        <button onClick={onAsk}>Pitaj</button>
      </div>
      {loading && <p className="muted">Razmišljam…</p>}
      {result?.error && <p className="muted">Greška: {result.error}</p>}
      {result && !result.error && result.sql && (
        <>
          <p className="muted">Generisani SQL:</p>
          <pre>{result.sql}</pre>
          {result.columns && result.rows && (
            <DataTable columns={result.columns} rows={result.rows} />
          )}
        </>
      )}
    </div>
  );
}
