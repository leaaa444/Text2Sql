from agent.config import settings
from agent.db.connection import run_query
from agent.nodes.guard import mask_pii, pii_column_indexes


def executor_node(state):
    try:
        columns, rows = run_query(state["sql"], limit=settings.result_limit)
    except Exception as exc:
        trace = state.get("trace", []) + [{"node": "executor", "info": f"greska: {exc}"}]
        return {"error": str(exc), "trace": trace}

    masked_rows = mask_pii(columns, rows)
    note = f"{len(rows)} redova"
    if pii_column_indexes(columns):
        note += " (PII maskiran)"
    trace = state.get("trace", []) + [{"node": "executor", "info": note}]
    return {"columns": columns, "rows": masked_rows, "trace": trace}
