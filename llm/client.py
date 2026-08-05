import os

from dotenv import load_dotenv
from litellm import acompletion

load_dotenv()


class LLMClient:

    def __init__(self):

        self.model = os.getenv(
            "LLM_MODEL",
            "anthropic/claude-sonnet-4-6"
        )

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = await acompletion(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.1
        )

        return response.choices[0].message.content