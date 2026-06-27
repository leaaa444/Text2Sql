import sqlglot
from sqlglot import exp

from agent.config import settings

_PII_HINTS = ("email", "mail", "phone", "telefon", "lozinka", "password")


def _enforce_limit(select, cap):
    limit = select.args.get("limit")
    current = None
    if limit is not None and isinstance(limit.expression, exp.Literal):
        try:
            current = int(limit.expression.this)
        except (TypeError, ValueError):
            current = None
    if current is None or current > cap:
        select = select.limit(cap)
    return select.sql(dialect="postgres")


def pii_column_indexes(columns):
    return [
        i
        for i, name in enumerate(columns)
        if any(hint in name.lower() for hint in _PII_HINTS)
    ]


def _mask_value(value):
    text = str(value)
    if "@" in text:
        name, _, domain = text.partition("@")
        masked = (name[0] + "***") if name else "***"
        return f"{masked}@{domain}"
    if len(text) <= 2:
        return "***"
    return text[0] + "***" + text[-1]


def mask_pii(columns, rows):
    idx = pii_column_indexes(columns)
    if not idx:
        return rows
    result = []
    for row in rows:
        row = list(row)
        for i in idx:
            if row[i] is not None:
                row[i] = _mask_value(row[i])
        result.append(row)
    return result


def guard_node(state):
    sql = state.get("sql", "")
    blocked_reason = None

    try:
        statements = sqlglot.parse(sql, dialect="postgres")
    except Exception:
        statements = []
        blocked_reason = "SQL ne moze da se parsira"

    if blocked_reason is None:
        if len(statements) != 1:
            blocked_reason = "dozvoljen je samo jedan upit"
        elif not isinstance(statements[0], exp.Select):
            blocked_reason = "dozvoljeni su samo SELECT upiti (citanje)"

    if blocked_reason:
        trace = state.get("trace", []) + [
            {"node": "guard", "info": f"BLOKIRANO: {blocked_reason}"}
        ]
        return {"guard_error": blocked_reason, "trace": trace}

    safe_sql = _enforce_limit(statements[0], settings.result_limit)
    changed = safe_sql.strip() != sql.strip()
    info = "bezbedan, +LIMIT" if changed else "bezbedan"
    trace = state.get("trace", []) + [{"node": "guard", "info": info}]
    return {"sql": safe_sql, "guard_error": None, "trace": trace}
