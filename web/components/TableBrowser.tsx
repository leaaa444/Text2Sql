"use client";

import { useEffect, useState } from "react";
import { getTables, getTableData, type TableData } from "@/lib/api";
import DataTable from "@/components/DataTable";

export default function TableBrowser() {
  const [tables, setTables] = useState<string[]>([]);
  const [active, setActive] = useState<string | null>(null);
  const [data, setData] = useState<TableData | null>(null);

  useEffect(() => {
    getTables()
      .then(setTables)
      .catch(() => setTables([]));
  }, []);

  async function show(name: string) {
    setActive(name);
    setData(null);
    setData(await getTableData(name));
  }

  return (
    <div className="card">
      <h2>Tabele u bazi</h2>
      <div>
        {tables.length === 0 && <span className="muted">Učitavam…</span>}
        {tables.map((t) => (
          <button key={t} className="secondary" onClick={() => show(t)}>
            {t}
          </button>
        ))}
      </div>
      {active && data && (
        <>
          <h3>{active}</h3>
          <DataTable columns={data.columns} rows={data.rows} />
        </>
      )}
    </div>
  );
}
