from typing import Any

from pydantic import BaseModel, Field
from planner.schemas import ResearchPlan

class ExecutorState(BaseModel):
    """
    Runtime state shared across the executor.
    """

    query: str

    research_plan: ResearchPlan

    completed_tasks: list[int] = Field(default_factory=list)

    task_results: dict[int, Any] = Field(default_factory=dict)

    metadata: dict[str, Any] = Field(default_factory=dict)