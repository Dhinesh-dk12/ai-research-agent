from llm.client import (
    LLMClient,
)

from report.prompt import (
    REPORT_SYSTEM_PROMPT,
)

from utils.logger import (
    logger,
)


class ReportService:

    def __init__(self):

        self.client = (
            LLMClient()
        )

    async def generate_report(

        self,

        query: str,

        reasoning_output: str,

    ) -> str:

        logger.info(
            "Generating research report..."
        )

        user_prompt = f"""
User Query:

{query}

Reasoning Output:

{reasoning_output}


"""

        report = await self.client.generate(

            system_prompt=REPORT_SYSTEM_PROMPT,

            user_prompt=user_prompt,

        )

        logger.success(
            "Research report generated."
        )

        return report