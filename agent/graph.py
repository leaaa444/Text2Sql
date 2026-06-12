from langgraph.graph import END, START, StateGraph

from agent.nodes.deliberator import deliberator_node
from agent.nodes.executor import executor_node
from agent.nodes.planner import planner_node
from agent.nodes.retriever import retriever_node
from agent.state import AgentState


def _build():
    builder = StateGraph(AgentState)
    builder.add_node("retriever", retriever_node)
    builder.add_node("planner", planner_node)
    builder.add_node("deliberator", deliberator_node)
    builder.add_node("executor", executor_node)
    builder.add_edge(START, "retriever")
    builder.add_edge("retriever", "planner")
    builder.add_edge("planner", "deliberator")
    builder.add_edge("deliberator", "executor")
    builder.add_edge("executor", END)
    return builder.compile()


graph = _build()


def answer(question):
    final = graph.invoke({"question": question, "trace": []})
    return {
        "plan": final.get("plan", []),
        "sql": final.get("sql", ""),
        "columns": final.get("columns", []),
        "rows": final.get("rows", []),
        "error": final.get("error"),
        "trace": final.get("trace", []),
    }


if __name__ == "__main__":
    import sys

    from tabulate import tabulate

    sys.stdout.reconfigure(encoding="utf-8")
    question = sys.argv[1] if len(sys.argv) > 1 else "Koja tri proizvoda su najskuplja?"
    out = answer(question)
    print("Plan:")
    for step in out["plan"]:
        print("  -", step)
    print("\nSQL:")
    print(out["sql"])
    if out["error"]:
        print("\nGreska:", out["error"])
    else:
        print()
        print(tabulate(out["rows"], headers=out["columns"], tablefmt="github"))
