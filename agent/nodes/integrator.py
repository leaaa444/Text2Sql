import sqlglot
from sqlglot import exp

from agent import ablation
from agent.db.schema import get_table_names


def integrator_node(state):
    if not ablation.current.use_integrator:
        trace = state.get("trace", []) + [{"node": "integrator", "info": "iskljucen"}]
        return {"validation_error": None, "trace": trace}
    sql = state.get("sql", "")
    problems = []

    try:
        parsed = sqlglot.parse_one(sql, dialect="postgres")
    except Exception as exc:
        parsed = None
        problems.append(f"SQL ne moze da se parsira ({exc})")

    if parsed is not None:
        known = {name.lower() for name in get_table_names()}
        used = set()
        for table in parsed.find_all(exp.Table):
            if (table.db or "").lower() == "information_schema":
                continue
            used.add(table.name.lower())
        unknown = used - known
        if unknown:
            problems.append(f"nepoznate tabele: {', '.join(sorted(unknown))}")

    validation_error = "; ".join(problems) if problems else None
    info = "validan" if validation_error is None else validation_error
    trace = state.get("trace", []) + [{"node": "integrator", "info": info}]
    return {"validation_error": validation_error, "trace": trace}
