from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    schema: str
    plan: list[str]
    sql: str
    columns: list[str]
    rows: list[list[Any]]
    error: str
    trace: list[dict]
