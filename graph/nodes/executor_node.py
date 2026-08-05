from graph.state import (
    ResearchState,
)

from executor.service import (
    ExecutorService,
)


executor = (
    ExecutorService()
)


async def executor_node(
    state: ResearchState,
) -> ResearchState:

    completed_tasks, task_results = (
        await executor.execute(

            research_plan=state[
                "research_plan"
            ],

        )
    )

    state[
        "completed_tasks"
    ] = completed_tasks

    state[
        "task_results"
    ] = task_results

    return state