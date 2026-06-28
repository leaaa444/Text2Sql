import difflib

_skills = [
    {
        "question": "Koliko ima kupaca?",
        "sql": "SELECT COUNT(*) FROM customers",
    },
    {
        "question": "Koja tri proizvoda su najskuplja?",
        "sql": "SELECT name, price FROM products ORDER BY price DESC LIMIT 3",
    },
    {
        "question": "Koliko narudzbina ima svaki kupac?",
        "sql": (
            "SELECT c.name, COUNT(o.id) FROM customers c "
            "LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.name"
        ),
    },
]


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
