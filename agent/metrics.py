from langchain_core.callbacks import BaseCallbackHandler


class _CallCounter(BaseCallbackHandler):
    def __init__(self):
        self.llm_calls = 0

    def on_chat_model_start(self, *args, **kwargs):
        self.llm_calls += 1


counter = _CallCounter()


def reset():
    counter.llm_calls = 0
