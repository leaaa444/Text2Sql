from agent import ablation
from agent.llm import get_llm

SYSTEM = (
    "You rewrite a follow-up question into a single, clear, self-contained question "
    "using the previous conversation. Keep the original intent; only fill in what the "
    "follow-up refers to. Resolve pronouns and references such as 'on', 'ona', 'njemu', "
    "'njih', 'taj', 'od njih' to the concrete person, item or set named in the previous "
    "questions and answers. If the question is already self-contained, return it unchanged. "
    "Copy names, values and numbers exactly as they are written in the conversation, "
    "keeping their letter case. Answer in the same language. Return only the rewritten "
    "question.\n\n"
    "Example:\n"
    "Previous question: Koliko filmova ima?\n"
    "Follow-up: a samo iz 2006. godine?\n"
    "Rewritten: Koliko filmova je iz 2006. godine?\n\n"
    "Example:\n"
    "Previous question: Ko je potrosio najvise para?\n"
    "Previous answer: Najvise je potrosio kupac KARL SEAL, ukupno 221.55.\n"
    "Follow-up: koje filmove je on uzimao?\n"
    "Rewritten: Koje filmove je iznajmljivao kupac KARL SEAL?"
)


def _turn_text(turn):
    text = f"Previous question: {turn['question']}"
    answer = (turn.get("answer") or "").strip()
    if answer:
        text += f"\nPrevious answer: {answer[:300]}"
    return text


def selector_node(state):
    question = state["question"]
    history = state.get("history", [])

    if not ablation.current.use_selector:
        trace = state.get("trace", []) + [{"node": "selector", "info": "iskljucen"}]
        return {"goal": question, "trace": trace}

    if not history:
        trace = state.get("trace", []) + [
            {"node": "selector", "info": "samostalno pitanje, bez izmene"}
        ]
        return {"goal": question, "trace": trace}

    history_text = "\n\n".join(_turn_text(h) for h in history[-3:])
    llm = get_llm()
    user = f"{history_text}\n\nFollow-up: {question}\n\nRewritten:"
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    goal = response.content.strip()

    if goal.strip().lower() == question.strip().lower():
        info = "samostalno pitanje, bez izmene"
    else:
        info = f"nastavno pitanje -> '{goal}'"
    trace = state.get("trace", []) + [{"node": "selector", "info": info}]
    return {"goal": goal, "trace": trace}
