#read the strucute of the database and create a description of the schema

from agent.db.connection import run_query

_BASE_TABLES_SQL = """
select c.relname
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind in ('r', 'p')
  and c.relispartition = false
order by c.relname
"""

_COLUMNS_SQL = """
select table_name, column_name, data_type
from information_schema.columns
where table_schema = 'public'
order by table_name, ordinal_position
"""

_FK_SQL = """
select
  con.conrelid::regclass::text as table_name,
  att.attname as column_name,
  con.confrelid::regclass::text as foreign_table,
  fatt.attname as foreign_column
from pg_constraint con
join pg_namespace ns on ns.oid = con.connamespace
join unnest(con.conkey) with ordinality as ck(attnum, ord) on true
join pg_attribute att
  on att.attrelid = con.conrelid and att.attnum = ck.attnum
join unnest(con.confkey) with ordinality as fk(attnum, ord) on fk.ord = ck.ord
join pg_attribute fatt
  on fatt.attrelid = con.confrelid and fatt.attnum = fk.attnum
where con.contype = 'f' and ns.nspname = 'public'
order by table_name
"""


def get_schema_text():
    allowed = set(get_table_names())
    _, column_rows = run_query(_COLUMNS_SQL)
    tables = {}
    for table, column, data_type in column_rows:
        if table not in allowed:
            continue
        tables.setdefault(table, []).append(f"{column} {data_type}")

    _, fk_rows = run_query(_FK_SQL)
    fks = [r for r in fk_rows if r[0] in allowed and r[2] in allowed]

    lines = [f"{table}(" + ", ".join(cols) + ")" for table, cols in tables.items()]
    if fks:
        lines.append("")
        lines.append("Foreign keys:")
        for table, column, ftable, fcolumn in fks:
            lines.append(f"  {table}.{column} -> {ftable}.{fcolumn}")
    return "\n".join(lines)


def get_table_names():
    _, rows = run_query(_BASE_TABLES_SQL)
    return [row[0] for row in rows]
