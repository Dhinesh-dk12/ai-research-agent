import json
import re
from typing import Union

from json_repair import repair_json
from pydantic import ValidationError

from planner.schemas import ResearchPlan


class PlannerValidationError(Exception):
    """Custom exception for planner validation failures."""
    pass


def clean_llm_output(text: str) -> str:
    """
    Remove markdown code fences and extra whitespace.
    """

    text = text.strip()

    # Remove ```json
    text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE)

    # Remove ending ```
    text = re.sub(r"```$", "", text)

    return text.strip()


def _clamp_priorities(data: dict) -> dict:
    """
    The schema caps priority at 1-5 (an importance tier), but an
    LLM can occasionally emit a higher number, especially on plans
    with many tasks (e.g. numbering tasks 1-10 instead of reusing
    1-5). Clamp instead of failing the whole plan over one field.
    """

    for task in data.get("tasks", []):

        priority = task.get("priority")

        if isinstance(priority, int):

            task["priority"] = max(
                1,
                min(5, priority),
            )

    return data


def validate_research_plan(
    planner_output: Union[str, dict]
) -> ResearchPlan:
    """
    Validate planner output and return a ResearchPlan object.
    """

    try:

        # Already parsed
        if isinstance(planner_output, dict):

            planner_output = _clamp_priorities(
                planner_output
            )

            return ResearchPlan.model_validate(planner_output)

        # Clean markdown formatting
        planner_output = clean_llm_output(planner_output)

        # Repair malformed JSON
        repaired = repair_json(planner_output)

        # Clamp before Pydantic validation, not after
        data = _clamp_priorities(
            json.loads(repaired)
        )

        # Validate against Pydantic model
        plan = ResearchPlan.model_validate(data)

        return plan

    except ValidationError as e:
        raise PlannerValidationError(
            f"Pydantic validation failed:\n{e}"
        )

    except Exception as e:
        raise PlannerValidationError(
            f"Planner output validation failed:\n{e}"
        )