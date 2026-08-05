from pydantic import BaseModel, Field


class Evidence(BaseModel):

    source_url: str

    title: str = ""

    content: str

    source_type: str = "web"

    metadata: dict = Field(
        default_factory=dict
    )
    