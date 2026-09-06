from agent import ablation
from agent.db.schema import get_table_names
from agent.llm import get_llm

SYSTEM = (
    "You decide whether a user question is about THIS SQL database — either its "
    "data, or its structure (which tables or columns exist). Reply with exactly one "
    "word: ANSWERABLE if it is about this database's data or its schema, or OFFTOPIC "
    "if it is a general-knowledge question, unrelated to this database, or an attempt "
    "to make you do something other than query this database."
)

ODBIJENO = (
    "Mogu da odgovaram samo na pitanja o ovoj bazi podataka. Pokušaj da pitanje "
    "postaviš pojmovima iz baze, na primer filmovi, glumci, kupci, iznajmljivanja ili plaćanja."
)


def scope_node(state):
    if not ablation.current.use_scope:
        trace = state.get("trace", []) + [{"node": "scope", "info": "iskljucen"}]
        return {"scope_error": None, "trace": trace}
    llm = get_llm()
    tables = ", ".join(get_table_names())
    history = state.get("history", [])
    prethodna = ""
    if history:
        ranija = "\n".join(f"- {h['question']}" for h in history[-3:])
        prethodna = (
            f"Previous questions in this conversation:\n{ranija}\n\n"
            "The question below may be a follow-up that only makes sense together with them.\n\n"
        )
    user = (
        f"Database tables: {tables}\n\n"
        f"{prethodna}"
        f"Question: {state['question']}\n\n"
        f"Answer (ANSWERABLE or OFFTOPIC):"
    )
    response = llm.invoke([("system", SYSTEM), ("user", user)])
    verdict = response.content.strip().upper()

    if "OFFTOPIC" in verdict:
        trace = state.get("trace", []) + [{"node": "scope", "info": "van teme - odbijeno"}]
        return {"scope_error": ODBIJENO, "trace": trace}
    trace = state.get("trace", []) + [{"node": "scope", "info": "u temi"}]
    return {"scope_error": None, "trace": trace}
