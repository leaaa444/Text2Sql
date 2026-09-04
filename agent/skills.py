import difflib

_SEEDS = [
    {
        "question": "Koliko ima filmova?",
        "sql": "SELECT COUNT(*) FROM film",
    },
    {
        "question": "Kojih pet filmova je najduze?",
        "sql": "SELECT title, length FROM film ORDER BY length DESC LIMIT 5",
    },
    {
        "question": "Koliko iznajmljivanja ima svaki kupac?",
        "sql": (
            "SELECT c.first_name, c.last_name, COUNT(r.rental_id) FROM customer c "
            "LEFT JOIN rental r ON r.customer_id = c.customer_id "
            "GROUP BY c.customer_id, c.first_name, c.last_name"
        ),
    },
]
_skills = [dict(s) for s in _SEEDS]


def _similarity(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def retrieve(question, k=2):
    ranked = sorted(
        _skills, key=lambda s: _similarity(question, s["question"]), reverse=True
    )
    return ranked[:k]


def add(question, sql):
    question = (question or "").strip()
    sql = (sql or "").strip()
    if not question or not sql:
        return
    for s in _skills:
        if s["question"].strip().lower() == question.lower():
            return
    _skills.append({"question": question, "sql": sql})


def reset():
    _skills[:] = [dict(s) for s in _SEEDS]
