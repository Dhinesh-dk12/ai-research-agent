from planner.schemas import (
    ResearchRequest,
)

from planner.service import (
    PlannerService,
)

from graph.state import (
    ResearchState,
)


planner = (
    PlannerService()
)


def planner_node(
    state: ResearchState,
) -> ResearchState:

    request = ResearchRequest(

        query=state["query"],

    )

    plan = planner.create_plan(
        request
    )

    state[
        "research_plan"
    ] = plan

    return state