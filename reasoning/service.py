from llm.client import LLMClient


class ReasoningService:

    def __init__(self):

        self.client = LLMClient()

    async def analyze(
        self,
        query,
        evidences,
    ):

        evidence_text = []

        citations = []

        for index, evidence in enumerate(
            evidences,
            start=1,
        ):

            evidence_text.append(

                f"""
SOURCE [{index}]

URL:
{evidence.source_url}

CONTENT:
{evidence.content}
"""
            )

            citations.append(
                f"[{index}] {evidence.source_url}"
            )

        prompt = f"""
User Query:
{query}

Evidence:

{chr(10).join(evidence_text)}

Instructions:

1. Analyze all evidence.
2. Use citations like [1], [2], [3] whenever making factual claims.
3. If multiple sources support a claim, cite them together.
   Example:
   - [1][4]
   - [2][3][7]
4. Never invent citations.
5. Use ONLY the evidence provided.
6. Preserve source credibility.
7. Mention limitations if evidence is insufficient.
8. Produce a concise but detailed reasoning output.
9. At the end of the reasoning output, include the REFERENCES section exactly as provided below.

REFERENCES

{chr(10).join(citations)}
"""

        response = await self.client.generate(

            system_prompt="""
You are a senior research analyst.

Your responsibilities:

- Analyze evidence critically.
- Produce factual and objective reasoning.
- Use citations consistently.
- Never fabricate information.
- Never invent references.
- Explicitly mention uncertainty when necessary.
""",

            user_prompt=prompt,

        )

        return response