from planner.schemas import (
    ResearchRequest,
    ResearchPlan,
    ResearchTask,
)

from planner.prompt import (
    PLANNER_SYSTEM_PROMPT,
)

from planner.client import generate

from planner.validator import (
    validate_research_plan,
)


class PlannerService:
    """
    Service responsible for generating and validating
    research plans.
    """

    @staticmethod
    def create_plan(
        request: ResearchRequest,
    ) -> ResearchPlan:

        messages = [
            {
                "role": "system",
                "content": PLANNER_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": request.model_dump_json(
                    indent=2
                ),
            },
        ]

        raw_response = generate(messages)

        print("\nRAW LLM RESPONSE:\n")
        print(raw_response)
        print("\n")

        validated_plan = (
            validate_research_plan(
                raw_response
            )
        )

        return validated_plan