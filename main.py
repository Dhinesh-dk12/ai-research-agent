import asyncio
import sys

from graph.workflow import (
    graph,
)

from graph.state import (
    ResearchState,
)


sif sys.platform.startswith(
    "win"
):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


async def main():

    initial_state: ResearchState = {

        # -----------------------------
        # User Input
        # -----------------------------

        "query":
        "give me detailed research report about future of humanoid robotic development.",

        # -----------------------------
        # Planner
        # -----------------------------

        "research_plan": None,

        # -----------------------------
        # Executor
        # -----------------------------

        "completed_tasks": [],

        "task_results": {},

        "metadata": {},

        # -----------------------------
        # Extraction
        # -----------------------------

        "urls": [],

        "fresh_evidences": [],

        # -----------------------------
        # Memory
        # -----------------------------

        "evidences": [],

        # -----------------------------
        # Reasoning
        # -----------------------------

        "reasoning_output": "",

        # -----------------------------
        # Report
        # -----------------------------

        "report": "",

        # -----------------------------
        # PDF
        # -----------------------------

        "pdf_path": "",

    }

    final_state = await graph.ainvoke(
        initial_state
    )

    print(
        "\n\nFINAL REPORT\n"
    )

    print(
        final_state[
            "report"
        ]
    )

    print(
        "\nPDF Saved To:\n"
    )

    print(
        final_state[
            "pdf_path"
        ]
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )