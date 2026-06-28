from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    schema: str
    history: list[dict]
    goal: str
    plan: list[str]
    sql: str
    validation_error: str
    guard_error: str
    scope_error: str
    columns: list[str]
    rows: list[list[Any]]
    summary: str
    error: str
    retry_count: int
    trace: list[dict]
