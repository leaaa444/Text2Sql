import re

from agent import ablation
from agent.db.schema import get_table_names
from agent.llm import get_llm

SYSTEM = (
    "You are a planning assistant for a text-to-SQL system. Given the database "
    "tables and a question, break the task into a short numbered list of concrete "
    "steps needed to build one SQL query (1-4 steps). Return only the steps, one "
    "per line. Write the steps in the same language as the question."
)


def _parse_steps(text):
    steps = []
    for line in text.splitlines():
        cleaned = re.sub(r"^\s*(\d+[.)]|[-*])\s*", "", line).strip()
        if cleaned:
            steps.append(cleaned)
    return steps or [text.strip()]


def planner_node(state):
    if not ablation.current.use_planner:
        trace = state.get("trace", []) + [{"node": "planner", "info": "iskljucen"}]
        return {"plan": [], "trace": trace}
    llm = get_llm()
    goal = state.get("goal") or state["question"]
    tables = ", ".join(get_table_names())
    user = f"Database tables: {tables}\n\nQuestion: {goal}\n\nSteps:"
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    steps = _parse_steps(response.content)
    trace = state.get("trace", []) + [{"node": "planner", "info": f"{len(steps)} korak(a)"}]
    return {"plan": steps, "trace": trace}
