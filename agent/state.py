from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    schema: str
    history: list[dict]
    plan: list[str]
    sql: str
    validation_error: str
    columns: list[str]
    rows: list[list[Any]]
    error: str
    retry_count: int
    trace: list[dict]
