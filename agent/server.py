from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import baseline
from agent.db.connection import run_query
from agent.db.schema import get_schema_text

app = FastAPI(title="text2sql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


def _clean(value):
    if value is None or isinstance(value, (int, float, bool, str)):
        return value
    return str(value)


def _list_tables():
    _, rows = run_query(
        "select table_name from information_schema.tables "
        "where table_schema = 'public' order by table_name"
    )
    return [r[0] for r in rows]


@app.get("/")
def root():
    return {"status": "ok", "frontend": "http://localhost:3000"}


@app.get("/api/tables")
def api_tables():
    return {"tables": _list_tables()}


@app.get("/api/schema")
def api_schema():
    return {"schema": get_schema_text()}


@app.get("/api/tables/{name}")
def api_table_data(name: str):
    if name not in _list_tables():
        raise HTTPException(status_code=404, detail="Nepoznata tabela")
    columns, rows = run_query(f'select * from "{name}"', limit=200)
    return {"columns": columns, "rows": [[_clean(v) for v in row] for row in rows]}


@app.post("/api/ask")
def api_ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Prazno pitanje")
    try:
        sql, columns, rows = baseline.answer(question)
    except Exception as exc:
        return {"error": str(exc)}
    return {"sql": sql, "columns": columns, "rows": [[_clean(v) for v in row] for row in rows]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
