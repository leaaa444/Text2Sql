from agent import ablation
from agent import memory


def recorder_load_node(state):
    if not ablation.current.use_recorder:
        trace = state.get("trace", []) + [{"node": "recorder_load", "info": "iskljucen"}]
        return {"history": [], "trace": trace}
    history = memory.load_history()
    trace = state.get("trace", []) + [
        {"node": "recorder_load", "info": f"{len(history)} prethodnih pitanja"}
    ]
    return {"history": history, "trace": trace}


def recorder_save_node(state):
    if not ablation.current.use_recorder:
        trace = state.get("trace", []) + [{"node": "recorder_save", "info": "iskljucen"}]
        return {"trace": trace}
    memory.save_turn(state.get("question", ""), state.get("sql", ""), state.get("summary", ""))
    trace = state.get("trace", []) + [{"node": "recorder_save", "info": "zapamceno pitanje"}]
    return {"trace": trace}
