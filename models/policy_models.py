from typing import List, Literal
from pydantic import BaseModel, Field


class PolicyFinding(BaseModel):
    """
    A single policy compliance finding.
    """

    policy_name: str = Field(
        description="Name of the policy document."
    )

    status: Literal[
        "COMPLIANT",
        "NEEDS_REVIEW",
        "NON_COMPLIANT",
    ] = Field(
        description="Compliance status for this policy."
    )

    explanation: str = Field(
        description="Explanation of the finding."
    )

    evidence: str = Field(
        description="Relevant policy excerpt supporting the finding."
    )


class PolicyReview(BaseModel):
    """
    Overall policy compliance review.
    """

    overall_status: Literal[
        "COMPLIANT",
        "NEEDS_REVIEW",
        "NON_COMPLIANT",
    ] = Field(
        description=(
            "Overall policy assessment. "
            "COMPLIANT if all policies are satisfied, "
            "NEEDS_REVIEW if manual review is required, "
            "NON_COMPLIANT if one or more critical policy violations exist."
        )
    )

    findings: List[PolicyFinding] = Field(
        default_factory=list,
        description="Only policy findings requiring reviewer attention."
    )

    summary: str = Field(
        description="Overall summary of the policy review."
    )