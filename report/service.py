from llm.client import LLMClient

from report.prompt import (
    REPORT_SYSTEM_PROMPT
)


class ReportService:

    def __init__(self):

        self.llm = LLMClient()

    async def generate_report(
        self,
        query: str,
        reasoning_output: str,
    ):

        user_prompt = f"""
Research Question:

{query}


Reasoning Output:

{reasoning_output}
"""

        report = await self.llm.generate(
            system_prompt=REPORT_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        return report