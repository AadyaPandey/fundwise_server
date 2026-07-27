from pydantic import BaseModel, Field


class QualityReview(BaseModel):
    """
    Final output produced by the Quality Reviewer Agent.
    """

    passed: bool = Field(
        ...,
        description="Whether the execution quality is acceptable."
    )

    coverage_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of required tools successfully executed."
    )

    evidence_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Quality of evidence returned by tools."
    )

    confidence_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall confidence in the execution."
    )

    missing_required_tools: list[str] = Field(default_factory=list)

    failed_tools: list[str] = Field(default_factory=list)

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    summary: str


