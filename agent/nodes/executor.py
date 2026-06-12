from agent.config import settings
from agent.db.connection import run_query


def executor_node(state):
    try:
        columns, rows = run_query(state["sql"], limit=settings.result_limit)
    except Exception as exc:
        trace = state.get("trace", []) + [{"node": "executor", "info": f"greska: {exc}"}]
        return {"error": str(exc), "trace": trace}
    trace = state.get("trace", []) + [{"node": "executor", "info": f"{len(rows)} redova"}]
    return {"columns": columns, "rows": rows, "trace": trace}
