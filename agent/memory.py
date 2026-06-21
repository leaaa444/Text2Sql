_history = []


def load_history():
    return list(_history)


def save_turn(question, sql):
    _history.append({"question": question, "sql": sql})


def reset():
    _history.clear()
