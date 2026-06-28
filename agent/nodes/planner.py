import re

from agent.llm import get_llm

SYSTEM = (
    "You are a planning assistant for a text-to-SQL system. Given a database "
    "schema and a question, break the task into a short numbered list of concrete "
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
    llm = get_llm()
    goal = state.get("goal") or state["question"]
    user = f"Database schema:\n{state['schema']}\n\nQuestion: {goal}\n\nSteps:"
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    steps = _parse_steps(response.content)
    trace = state.get("trace", []) + [{"node": "planner", "info": f"{len(steps)} korak(a)"}]
    return {"plan": steps, "trace": trace}
