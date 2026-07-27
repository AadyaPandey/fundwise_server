from typing import Literal
from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    tool: Literal[
        "registration",
        "eligibility",
        "budget",
        # "policy_rag",
        "documentation"
        # "duplicate",
        # "risk",
    ]

    reason: str = Field(
        description="Why this tool should be executed."
    )
    required: bool = True


class ExecutionPlan(BaseModel):
    steps: list[PlanStep]