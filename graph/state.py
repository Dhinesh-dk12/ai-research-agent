from typing import Any

from typing_extensions import TypedDict

from planner.schemas import (
    ResearchPlan,
)

from research.evidence import (
    Evidence,
)


class ResearchState(TypedDict):
    """
    Shared state for the LangGraph workflow.

    Every node reads the fields it needs and
    writes only the fields it produces.
    """

    # --------------------------------------------------
    # User Input
    # --------------------------------------------------

    query: str

    # --------------------------------------------------
    # Planner Output
    # --------------------------------------------------

    research_plan: ResearchPlan

    # --------------------------------------------------
    # Executor Output
    # --------------------------------------------------

    completed_tasks: list[int]

    task_results: dict[int, Any]

    metadata: dict[str, Any]

    # --------------------------------------------------
    # Extraction Output
    # --------------------------------------------------

    urls: list[str]

    fresh_evidences: list[Evidence]

    # --------------------------------------------------
    # Memory Output
    # --------------------------------------------------

    evidences: list[Evidence]

    # --------------------------------------------------
    # Reasoning Output
    # --------------------------------------------------

    reasoning_output: str

    # --------------------------------------------------
    # Report Output
    # --------------------------------------------------

    report: str

    # --------------------------------------------------
    # PDF Output
    # --------------------------------------------------

    pdf_path: str