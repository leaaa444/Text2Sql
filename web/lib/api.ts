export type Cell = string | number | boolean | null;

export type TableData = {
  columns: string[];
  rows: Cell[][];
};

export type AskResult = {
  sql?: string;
  columns?: string[];
  rows?: Cell[][];
  error?: string;
};

export async function getTables(): Promise<string[]> {
  const res = await fetch("/api/tables");
  const data = await res.json();
  return data.tables;
}

export async function getTableData(name: string): Promise<TableData> {
  const res = await fetch(`/api/tables/${encodeURIComponent(name)}`);
  return res.json();
}

export async function ask(question: string): Promise<AskResult> {
  const res = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return res.json();
}
