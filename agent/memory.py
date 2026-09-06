_history = []


def load_history():
    return list(_history)


def save_turn(question, sql, answer=""):
    _history.append({"question": question, "sql": sql, "answer": answer})


def reset():
    _history.clear()
