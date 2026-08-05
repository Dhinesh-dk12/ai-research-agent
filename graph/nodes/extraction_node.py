from graph.state import (
    ResearchState,
)

from research.extraction_service import (
    ExtractionService,
)


extraction = (
    ExtractionService()
)


async def extraction_node(
    state: ResearchState,
) -> ResearchState:

    urls, fresh_evidences = (
        await extraction.extract(

            task_results=state[
                "task_results"
            ],

        )
    )

    state[
        "urls"
    ] = urls

    state[
        "fresh_evidences"
    ] = fresh_evidences

    state[
        "evidences"
    ] = fresh_evidences.copy()

    return state