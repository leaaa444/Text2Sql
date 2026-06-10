import sys

from tabulate import tabulate

from agent.config import settings
from agent.db.connection import run_query
from agent.db.schema import get_schema_text
from agent.llm import get_llm

SYSTEM = (
    "You are an expert data analyst who writes PostgreSQL queries. "
    "Given a database schema and a question, return a single valid PostgreSQL "
    "SELECT query that answers it. Return only the SQL, with no explanation and "
    "no markdown fences."
)


def extract_sql(text):
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        if len(parts) > 1:
            text = parts[1].strip()
        if text.lower().startswith("sql"):
            text = text[3:].strip()
    return text.strip().rstrip(";").strip()


def generate_sql(question, schema_text=None, provider=None, model=None):
    if schema_text is None:
        schema_text = get_schema_text()
    llm = get_llm(provider, model)
    user = f"Database schema:\n{schema_text}\n\nQuestion: {question}\n\nSQL:"
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    return extract_sql(response.content)


def answer(question, provider=None, model=None):
    schema_text = get_schema_text()
    sql = generate_sql(question, schema_text, provider, model)
    columns, rows = run_query(sql, limit=settings.result_limit)
    return sql, columns, rows


def main():
    if len(sys.argv) < 2:
        print('Upotreba: python -m agent.baseline "pitanje na prirodnom jeziku"')
        return
    question = sys.argv[1]
    sql, columns, rows = answer(question)
    print("SQL:")
    print(sql)
    print()
    print(tabulate(rows, headers=columns, tablefmt="github"))


if __name__ == "__main__":
    main()
