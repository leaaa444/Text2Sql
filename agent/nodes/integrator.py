import sqlglot
from sqlglot import exp

from agent.db.schema import get_table_names


def integrator_node(state):
    sql = state.get("sql", "")
    problems = []

    try:
        parsed = sqlglot.parse_one(sql, dialect="postgres")
    except Exception as exc:
        parsed = None
        problems.append(f"SQL ne moze da se parsira ({exc})")

    if parsed is not None:
        known = {name.lower() for name in get_table_names()}
        used = {table.name.lower() for table in parsed.find_all(exp.Table)}
        unknown = used - known
        if unknown:
            problems.append(f"nepoznate tabele: {', '.join(sorted(unknown))}")

    validation_error = "; ".join(problems) if problems else None
    info = "validan" if validation_error is None else validation_error
    trace = state.get("trace", []) + [{"node": "integrator", "info": info}]
    return {"validation_error": validation_error, "trace": trace}
