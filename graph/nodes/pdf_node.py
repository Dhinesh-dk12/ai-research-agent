import os

from graph.state import (
    ResearchState,
)

from report.pdf_service import (
    PDFService,
)

from utils.logger import (
    logger,
)


pdf_service = PDFService()


def pdf_node(
    state: ResearchState,
) -> ResearchState:

    logger.info(
        "Generating PDF report..."
    )

    os.makedirs(
        "reports",
        exist_ok=True,
    )

    pdf_path = (
        "reports/final_report.pdf"
    )

    with open(
        "reports/final_report.md",
        "w",
        encoding="utf-8",
    ) as report_file:

        report_file.write(
            state["report"]
        )

    pdf_service.generate_pdf(

        markdown_text=state[
            "report"
        ],

        output_path=pdf_path,

    )

    state[
        "pdf_path"
    ] = pdf_path

    logger.success(
        f"PDF saved to {pdf_path}"
    )

    return state