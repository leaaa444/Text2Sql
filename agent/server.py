from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import graph as agent_graph
from agent import memory
from agent import suggestions
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


def _friendly_error(exc):
    text = str(exc).lower()
    if any(k in text for k in ("rate_limit", "429", "tokens per", "resource_exhausted", "quota")):
        return (
            "Trenutno je previše zahteva prema jezičkom modelu "
            "(ograničenje besplatnog naloga). Sačekajte nekoliko sekundi pa pokušajte ponovo."
        )
    if "timeout" in text or "timed out" in text:
        return "Jezički model nije odgovorio na vreme. Pokušajte ponovo."
    if "connection" in text or "network" in text or "getaddrinfo" in text:
        return "Problem sa mrežnom vezom. Proverite internet i pokušajte ponovo."
    if "api_key" in text or "unauthorized" in text or "authentication" in text:
        return "Problem sa pristupom jezičkom modelu (API ključ). Proverite podešavanja."
    return "Došlo je do greške pri obradi pitanja. Pokušajte ponovo."


def _list_tables():
    _, rows = run_query(
        "select table_name from information_schema.tables "
        "where table_schema = 'public' order by table_name"
    )
    return [r[0] for r in rows]


@app.get("/")
def root():
    return {"status": "ok", "frontend": "http://localhost:3000"}


@app.post("/api/reset")
def api_reset():
    memory.reset()
    return {"status": "ok"}


@app.get("/api/suggestions")
def api_suggestions():
    return {"suggestions": suggestions.get_suggestions()}


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
        out = agent_graph.answer(question)
    except Exception as exc:
        return {"error": _friendly_error(exc)}
    answered = out["answered"]
    columns = out["columns"] if answered else []
    rows = out["rows"] if answered else []
    return {
        "summary": out["summary"],
        "plan": out["plan"],
        "sql": out["sql"],
        "columns": columns,
        "rows": [[_clean(v) for v in row] for row in rows],
        "answered": answered,
        "error": out["error"],
        "trace": out["trace"],
        "retry_count": out["retry_count"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
