from agent.db.schema import get_schema_text


def retriever_node(state):
    schema = get_schema_text()
    trace = state.get("trace", []) + [{"node": "retriever", "info": "ucitana sema baze"}]
    return {"schema": schema, "trace": trace}
