from agent import ablation
from agent.llm import get_llm

SYSTEM = (
    "You rewrite a follow-up question into a single, clear, self-contained question "
    "using the previous conversation. Keep the original intent; only fill in what the "
    "follow-up refers to. Answer in the same language. Return only the rewritten "
    "question.\n\n"
    "Example:\n"
    "Previous: Koliko filmova ima?\n"
    "Follow-up: a samo iz 2006. godine?\n"
    "Rewritten: Koliko filmova je iz 2006. godine?"
)

_FOLLOWUP_MARKERS = ("a ", "i ", "ali ", "samo ")


def _looks_like_followup(question):
    q = question.strip().lower()
    return q.startswith(_FOLLOWUP_MARKERS)


def selector_node(state):
    question = state["question"]
    history = state.get("history", [])

    if not ablation.current.use_selector:
        trace = state.get("trace", []) + [{"node": "selector", "info": "iskljucen"}]
        return {"goal": question, "trace": trace}

    if not history or not _looks_like_followup(question):
        trace = state.get("trace", []) + [
            {"node": "selector", "info": "samostalno pitanje, bez izmene"}
        ]
        return {"goal": question, "trace": trace}

    history_text = "\n".join(f"- {h['question']}" for h in history[-3:])
    llm = get_llm()
    user = (
        f"Previous questions:\n{history_text}\n\n"
        f"Follow-up: {question}\n\nRewritten:"
    )
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    goal = response.content.strip()

    trace = state.get("trace", []) + [
        {"node": "selector", "info": f"nastavno pitanje -> '{goal}'"}
    ]
    return {"goal": goal, "trace": trace}
