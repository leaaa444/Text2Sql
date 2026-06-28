from agent import skills
from agent.llm import get_llm

SYSTEM = (
    "You are a helpful data analyst. The result table already answers the question "
    "(it may be ordered or filtered as the user asked). Give a short, direct, "
    "confident answer in the same language as the question (1-2 sentences) based on "
    "the rows. Do not claim data is missing if the rows answer the question. Use "
    "only the data shown."
)


def presenter_node(state):
    columns = state.get("columns", [])
    rows = state.get("rows", [])
    header = " | ".join(columns)
    body = "\n".join(" | ".join(str(v) for v in row) for row in rows[:20])
    table_text = f"{header}\n{body}" if columns else "(prazno)"

    goal = state.get("goal") or state["question"]
    llm = get_llm()
    user = f"Question: {goal}\n\nResult table:\n{table_text}\n\nAnswer:"
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    summary = response.content.strip()
    skills.add(goal, state.get("sql", ""))

    trace = state.get("trace", []) + [{"node": "presenter", "info": "napisan sazetak"}]
    return {"summary": summary, "trace": trace}
