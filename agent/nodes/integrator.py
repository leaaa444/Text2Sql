import sqlglot
from sqlglot import exp

from agent import ablation
from agent.db.schema import get_foreign_keys, get_table_names


def _aliasi(parsed):
    mapa = {}
    for table in parsed.find_all(exp.Table):
        if (table.db or "").lower() == "information_schema":
            continue
        name = table.name.lower()
        alias = (table.alias or "").lower()
        mapa[name] = name
        if alias:
            mapa[alias] = name
    return mapa


def _spajanja(parsed, mapa):
    parovi = []
    for eq in parsed.find_all(exp.EQ):
        left, right = eq.left, eq.right
        if not (isinstance(left, exp.Column) and isinstance(right, exp.Column)):
            continue
        t_left = mapa.get((left.table or "").lower())
        t_right = mapa.get((right.table or "").lower())
        if not t_left or not t_right or t_left == t_right:
            continue
        parovi.append((t_left, left.name.lower(), t_right, right.name.lower()))
    return parovi


def _dozvoljeno(par, kljucevi):
    t1, c1, t2, c2 = par
    if c1 == c2:
        return True
    return (t1, c1, t2, c2) in kljucevi or (t2, c2, t1, c1) in kljucevi


def losa_spajanja(parsed):
    kljucevi = {
        (t.lower(), c.lower(), ft.lower(), fc.lower()) for t, c, ft, fc in get_foreign_keys()
    }
    mapa = _aliasi(parsed)
    return [par for par in _spajanja(parsed, mapa) if not _dozvoljeno(par, kljucevi)]


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
        else:
            losa = losa_spajanja(parsed)
            if losa:
                opis = "; ".join(f"{t1}.{c1} = {t2}.{c2}" for t1, c1, t2, c2 in losa)
                problems.append(
                    f"spajanje ne odgovara stranim kljucevima seme: {opis} "
                    "(koristi kolone povezane stranim kljucem, po potrebi preko medjutabele)"
                )

    validation_error = "; ".join(problems) if problems else None
    info = "validan" if validation_error is None else validation_error
    trace = state.get("trace", []) + [{"node": "integrator", "info": info}]
    return {"validation_error": validation_error, "trace": trace}
