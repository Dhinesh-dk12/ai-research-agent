from graph.state import (
    ResearchState,
)

from reasoning.service import (
    ReasoningService,
)


reasoning = (
    ReasoningService()
)


async def reasoning_node(
    state: ResearchState,
) -> ResearchState:

    reasoning_output = (
        await reasoning.analyze(

            query=state["query"],

            evidences=state[
                "evidences"
            ],

        )
    )

    state[
        "reasoning_output"
    ] = reasoning_output

    return state