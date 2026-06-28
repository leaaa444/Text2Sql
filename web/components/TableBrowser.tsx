"use client";

import { useEffect, useState } from "react";
import { getTables, getTableData, type TableData } from "@/lib/api";
import DataTable from "@/components/DataTable";

function plural(n: number) {
  const d = n % 10;
  const dd = n % 100;
  if (d === 1 && dd !== 11) return "red";
  if (d >= 2 && d <= 4 && (dd < 12 || dd > 14)) return "reda";
  return "redova";
}

export default function TableBrowser() {
  const [tables, setTables] = useState<string[]>([]);
  const [active, setActive] = useState<string | null>(null);
  const [data, setData] = useState<TableData | null>(null);
  const [loading, setLoading] = useState(false);

  async function show(name: string) {
    setActive(name);
    setData(null);
    setLoading(true);
    try {
      setData(await getTableData(name));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    getTables()
      .then((list) => {
        setTables(list);
        if (list.length > 0) show(list[0]);
      })
      .catch(() => setTables([]));
  }, []);

  return (
    <div className="browser">
      <aside className="table-list">
        <div className="table-list-title">Tabele</div>
        {tables.length === 0 && <span className="muted">Učitavam…</span>}
        {tables.map((t) => (
          <button
            key={t}
            className={`table-item ${active === t ? "active" : ""}`}
            onClick={() => show(t)}
          >
            {t}
          </button>
        ))}
      </aside>

      <section className="table-view card">
        {active && (
          <div className="table-view-head">
            <h3>{active}</h3>
            {data && (
              <span className="muted">
                {data.rows.length} {plural(data.rows.length)}
              </span>
            )}
          </div>
        )}
        {loading && <span className="muted">Učitavam…</span>}
        {!loading && data && <DataTable columns={data.columns} rows={data.rows} />}
        {!active && tables.length > 0 && (
          <span className="muted">Izaberi tabelu sa leve strane.</span>
        )}
      </section>
    </div>
  );
}
