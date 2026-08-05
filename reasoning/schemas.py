from pydantic import BaseModel


class ReasoningResult(BaseModel):

    summary: str

    key_findings: list[str]

    conclusions: str

    limitations: str