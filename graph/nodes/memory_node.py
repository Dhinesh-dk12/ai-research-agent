from graph.state import (
    ResearchState,
)

from memory.retrieval_service import (
    MemoryRetrievalService,
)


memory = (
    MemoryRetrievalService()
)


def memory_node(
    state: ResearchState,
) -> ResearchState:

    previous_evidences = (

        memory.retrieve(

            query=state["query"],

        )

    )

    state[
        "evidences"
    ].extend(

        previous_evidences

    )

    return state