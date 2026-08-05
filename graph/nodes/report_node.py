from graph.state import (
    ResearchState,
)

from report.service import (
    ReportService,
)

from utils.logger import (
    logger,
)


report_service = (
    ReportService()
)


async def report_node(
    state: ResearchState,
) -> ResearchState:

    logger.info(
        "Generating final report..."
    )

    report = (
        await report_service.generate_report(

            query=state["query"],

            reasoning_output=state[
                "reasoning_output"
            ],

        )
    )

    state[
        "report"
    ] = report

    logger.success(
        "Report generated successfully."
    )

    return state