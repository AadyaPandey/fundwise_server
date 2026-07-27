from enum import Enum

from pydantic import BaseModel, Field


class Decision(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class GrantDecision(BaseModel):
    decision: Decision

    confidence: float = Field(
        ge=0,
        le=100,
    )

    reasons: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    summary: str