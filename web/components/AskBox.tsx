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

      {result && (
        <>
          {result.plan && result.plan.length > 0 && (
            <>
              <p className="muted">Plan (koraci agenta):</p>
              <ol>
                {result.plan.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ol>
            </>
          )}

          {result.sql && (
            <>
              <p className="muted">Generisani SQL:</p>
              <pre>{result.sql}</pre>
            </>
          )}

          {result.error && <p className="muted">Greška: {result.error}</p>}

          {!result.error && result.columns && result.rows && (
            <DataTable columns={result.columns} rows={result.rows} />
          )}

          {result.trace && result.trace.length > 0 && (
            <>
              <p className="muted">
                Koraci agenta (iza kulisa)
                {result.retry_count ? ` · popravki: ${result.retry_count}` : ""}:
              </p>
              <ol>
                {result.trace.map((step, i) => (
                  <li key={i}>
                    <b>{step.node}</b> — {step.info}
                  </li>
                ))}
              </ol>
            </>
          )}
        </>
      )}
    </div>
  );
}
