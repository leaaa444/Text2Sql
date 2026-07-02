from agent import ablation
from agent.db.schema import get_schema_text


def retriever_node(state):
    if not ablation.current.use_retriever:
        trace = state.get("trace", []) + [{"node": "retriever", "info": "iskljucen"}]
        return {"schema": "", "trace": trace}
    schema = get_schema_text()
    trace = state.get("trace", []) + [{"node": "retriever", "info": "ucitana sema baze"}]
    return {"schema": schema, "trace": trace}
