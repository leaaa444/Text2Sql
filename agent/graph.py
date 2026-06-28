from langgraph.graph import END, START, StateGraph

from agent.config import settings
from agent.nodes.deliberator import deliberator_node
from agent.nodes.executor import executor_node
from agent.nodes.guard import guard_node
from agent.nodes.integrator import integrator_node
from agent.nodes.planner import planner_node
from agent.nodes.presenter import presenter_node
from agent.nodes.recorder import recorder_load_node, recorder_save_node
from agent.nodes.reflector import reflector_node
from agent.nodes.retriever import retriever_node
from agent.nodes.selector import selector_node
from agent.state import AgentState


def _route_after_integrator(state):
    if state.get("validation_error"):
        if state.get("retry_count", 0) < settings.max_retries:
            return "reflector"
        return "kraj"
    return "guard"


def _route_after_guard(state):
    if state.get("guard_error"):
        return "kraj"
    return "executor"


def _route_after_executor(state):
    if state.get("error"):
        if state.get("retry_count", 0) < settings.max_retries:
            return "reflector"
        return "kraj"
    return "presenter"


def _build():
    builder = StateGraph(AgentState)
    builder.add_node("recorder_load", recorder_load_node)
    builder.add_node("retriever", retriever_node)
    builder.add_node("selector", selector_node)
    builder.add_node("planner", planner_node)
    builder.add_node("deliberator", deliberator_node)
    builder.add_node("integrator", integrator_node)
    builder.add_node("reflector", reflector_node)
    builder.add_node("guard", guard_node)
    builder.add_node("executor", executor_node)
    builder.add_node("presenter", presenter_node)
    builder.add_node("recorder_save", recorder_save_node)

    builder.add_edge(START, "recorder_load")
    builder.add_edge("recorder_load", "retriever")
    builder.add_edge("retriever", "selector")
    builder.add_edge("selector", "planner")
    builder.add_edge("planner", "deliberator")
    builder.add_edge("deliberator", "integrator")
    builder.add_conditional_edges(
        "integrator",
        _route_after_integrator,
        {"reflector": "reflector", "guard": "guard", "kraj": "recorder_save"},
    )
    builder.add_conditional_edges(
        "guard",
        _route_after_guard,
        {"executor": "executor", "kraj": "recorder_save"},
    )
    builder.add_conditional_edges(
        "executor",
        _route_after_executor,
        {"reflector": "reflector", "presenter": "presenter", "kraj": "recorder_save"},
    )
    builder.add_edge("reflector", "integrator")
    builder.add_edge("presenter", "recorder_save")
    builder.add_edge("recorder_save", END)
    return builder.compile()


graph = _build()


def answer(question):
    final = graph.invoke({"question": question, "trace": []})
    error = (
        final.get("error")
        or final.get("validation_error")
        or final.get("guard_error")
    )
    return {
        "summary": final.get("summary", ""),
        "plan": final.get("plan", []),
        "sql": final.get("sql", ""),
        "columns": final.get("columns", []),
        "rows": final.get("rows", []),
        "error": error,
        "retry_count": final.get("retry_count", 0),
        "trace": final.get("trace", []),
    }


if __name__ == "__main__":
    import sys

    from tabulate import tabulate

    sys.stdout.reconfigure(encoding="utf-8")
    question = sys.argv[1] if len(sys.argv) > 1 else "Koja tri proizvoda su najskuplja?"
    out = answer(question)
    print("Odgovor:", out["summary"])
    print("\nSQL:")
    print(out["sql"])
    if out["error"]:
        print("\nGreska:", out["error"])
    else:
        print()
        print(tabulate(out["rows"], headers=out["columns"], tablefmt="github"))
