from agent import skills
from agent.baseline import extract_sql
from agent.llm import get_llm

SYSTEM = (
    "You are an expert that writes a single PostgreSQL SELECT query. Given a "
    "database schema, a question and a short plan, return only the SQL query, "
    "with no explanation and no markdown fences. Select the columns that answer "
    "the question, and also include any column used for ranking or filtering "
    "(for example, when asked for the most expensive items, also select the price). "
    "To list the database's tables or columns, query information_schema (e.g., "
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public')."
)


def deliberator_node(state):
    llm = get_llm()
    goal = state.get("goal") or state["question"]
    plan = "\n".join(f"- {step}" for step in state.get("plan", []))
    examples = skills.retrieve(goal, k=2)
    examples_text = "\n\n".join(
        f"Pitanje: {e['question']}\nSQL: {e['sql']}" for e in examples
    )
    examples_block = (
        f"Primeri ispravnih upita (uzori):\n{examples_text}\n\n" if examples_text else ""
    )
    user = (
        f"Database schema:\n{state['schema']}\n\n"
        f"{examples_block}"
        f"Question: {goal}\n\n"
        f"Plan:\n{plan}\n\nSQL:"
    )
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    sql = extract_sql(response.content)
    trace = state.get("trace", []) + [
        {"node": "deliberator", "info": f"generisan SQL ({len(examples)} primera)"}
    ]
    return {"sql": sql, "trace": trace}
