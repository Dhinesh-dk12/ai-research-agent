from llm.client import LLMClient

from summarizer.prompt import (
    SUMMARIZER_SYSTEM_PROMPT
)


class SummarizerService:

    def __init__(self):

        self.client = LLMClient()

    async def summarize(
        self,
        content: str,
    ) -> str:

        prompt = f"""
Summarize the following content.

CONTENT:

{content}
"""

        response = await self.client.generate(

            system_prompt=
            SUMMARIZER_SYSTEM_PROMPT,

            user_prompt=prompt,
        )

        return response