from agent import memory


def recorder_load_node(state):
    history = memory.load_history()
    trace = state.get("trace", []) + [
        {"node": "recorder_load", "info": f"{len(history)} prethodnih pitanja"}
    ]
    return {"history": history, "trace": trace}


def recorder_save_node(state):
    memory.save_turn(state.get("question", ""), state.get("sql", ""))
    trace = state.get("trace", []) + [{"node": "recorder_save", "info": "zapamceno pitanje"}]
    return {"trace": trace}
