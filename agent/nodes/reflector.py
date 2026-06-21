from agent.baseline import extract_sql
from agent.llm import get_llm

SYSTEM = (
    "You are an expert that fixes a broken PostgreSQL SELECT query. Given the "
    "database schema, the question, the previous (failed) SQL and the error "
    "message, return a corrected single PostgreSQL SELECT query. Return only the "
    "SQL, with no explanation and no markdown fences."
)


def reflector_node(state):
    error = state.get("validation_error") or state.get("error") or "nepoznata greska"
    llm = get_llm()
    user = (
        f"Database schema:\n{state['schema']}\n\n"
        f"Question: {state['question']}\n\n"
        f"Previous SQL:\n{state.get('sql', '')}\n\n"
        f"Error:\n{error}\n\n"
        f"Corrected SQL:"
    )
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    sql = extract_sql(response.content)
    retry_count = state.get("retry_count", 0) + 1
    trace = state.get("trace", []) + [
        {"node": "reflector", "info": f"popravka #{retry_count} (greska: {error})"}
    ]
    return {
        "sql": sql,
        "retry_count": retry_count,
        "validation_error": None,
        "error": None,
        "trace": trace,
    }
