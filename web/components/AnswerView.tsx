"use client";

import { useState } from "react";
import { type AskResult } from "@/lib/api";
import DataTable from "@/components/DataTable";

function renderStep(text: string) {
  return text.split(/"([^"]+)"/g).map((part, i) =>
    i % 2 === 1 ? (
      <code key={i} className="ident">
        {part}
      </code>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

export default function AnswerView({ result }: { result: AskResult }) {
  const [showDetails, setShowDetails] = useState(false);

  const hasDetails =
    Boolean(result.sql) ||
    (result.plan?.length ?? 0) > 0 ||
    (result.trace?.length ?? 0) > 0;

  return (
    <div>
      {result.error ? (
        <p className="error">⚠ {result.error}</p>
      ) : (
        <>
          {result.summary && <p className="answer-text">{result.summary}</p>}
          {result.columns && result.rows && result.rows.length > 0 && (
            <DataTable columns={result.columns} rows={result.rows} />
          )}
        </>
      )}

      {hasDetails && (
        <>
          <button className="info-btn" onClick={() => setShowDetails((v) => !v)}>
            {showDetails ? "Sakrij detalje" : "ℹ Koraci i SQL"}
          </button>

          {showDetails && (
            <div className="details">
              {result.sql && (
                <>
                  <div className="label">Generisani SQL</div>
                  <pre>{result.sql}</pre>
                </>
              )}
              {result.plan && result.plan.length > 0 && (
                <>
                  <div className="label">Plan</div>
                  <ol>
                    {result.plan.map((step, i) => (
                      <li key={i}>{renderStep(step)}</li>
                    ))}
                  </ol>
                </>
              )}
              {result.trace && result.trace.length > 0 && (
                <>
                  <div className="label">
                    Koraci agenta
                    {result.retry_count ? ` · popravki: ${result.retry_count}` : ""}
                  </div>
                  <ul className="steps">
                    {result.trace.map((step, i) => (
                      <li key={i}>
                        <b>{step.node}</b> {step.info}
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
