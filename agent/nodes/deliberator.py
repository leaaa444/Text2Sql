from agent.baseline import extract_sql
from agent.llm import get_llm

SYSTEM = (
    "You are an expert that writes a single PostgreSQL SELECT query. Given a "
    "database schema, a question and a short plan, return only the SQL query, "
    "with no explanation and no markdown fences."
)


def deliberator_node(state):
    llm = get_llm()
    plan = "\n".join(f"- {step}" for step in state.get("plan", []))
    history = state.get("history", [])
    history_text = "\n".join(
        f"Pitanje: {h['question']}\nSQL: {h['sql']}" for h in history[-3:]
    )
    history_block = (
        f"Prethodna pitanja i upiti (kontekst za nastavna pitanja):\n{history_text}\n\n"
        if history_text
        else ""
    )
    user = (
        f"Database schema:\n{state['schema']}\n\n"
        f"{history_block}"
        f"Question: {state['question']}\n\n"
        f"Plan:\n{plan}\n\nSQL:"
    )
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    sql = extract_sql(response.content)
    trace = state.get("trace", []) + [{"node": "deliberator", "info": "generisan SQL"}]
    return {"sql": sql, "trace": trace}
