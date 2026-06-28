import re

from agent.db.schema import get_schema_text
from agent.llm import get_llm

SYSTEM = (
    "You generate example questions a user could ask about a database. Given the "
    "schema, return 4 short, natural and diverse questions in Serbian (different "
    "tables and operations: counting, top-N, join, grouping). Return only the "
    "questions, one per line, no numbering and no extra text."
)

_cache = None


def _parse(text):
    out = []
    for line in text.splitlines():
        line = re.sub(r"^\s*(\d+[.)]|[-*])\s*", "", line).strip().strip('"')
        if line:
            out.append(line)
    return out[:4]


def get_suggestions():
    global _cache
    if _cache:
        return _cache
    schema = get_schema_text()
    llm = get_llm()
    user = f"Database schema:\n{schema}\n\nQuestions:"
    try:
        response = llm.invoke([("system", SYSTEM), ("user", user)])
        result = _parse(response.content)
    except Exception:
        result = []
    if result:
        _cache = result
    return result


def clear_cache():
    global _cache
    _cache = None
