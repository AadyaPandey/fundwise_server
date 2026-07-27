from pydantic import BaseModel, Field


class SecurityReview(BaseModel):
    """
    Output of the Security Reviewer Agent.
    Evaluates whether the application or workflow
    contains prompt injection, policy bypass,
    or other suspicious behavior.
    """

    safe: bool = Field(
        ...,
        description="Whether the workflow is considered safe."
    )

    injection_detected: bool = Field(
        ...,
        description="True if prompt injection is detected."
    )

    policy_bypass_detected: bool = Field(
        ...,
        description="True if policy bypass attempts are detected."
    )

    suspicious_instructions: bool = Field(
        ...,
        description="True if suspicious AI-directed instructions are found."
    )

    security_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall security confidence score."
    )

    threats: list[str] = Field(
        default_factory=list,
        description="Detected security threats."
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Security warnings."
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Suggested mitigation steps."
    )

    summary: str = Field(
        ...,
        description="Overall security assessment."
    )

class SecurityScanResult(BaseModel):
    """
    Output of the rule-based security scanner.
    """

    injection: list[str] = Field(default_factory=list)

    policy_bypass: list[str] = Field(default_factory=list)

    suspicious: list[str] = Field(default_factory=list)

    @property
    def has_threats(self) -> bool:
        return bool(
            self.injection
            or self.policy_bypass
            or self.suspicious
        )


from pydantic import BaseModel, Field


class GeminiSecurityAnalysis(BaseModel):
    safe: bool = Field(
        description="Whether the application appears safe."
    )

    security_score: int = Field(
        ge=0,
        le=100,
        description="Overall security confidence score."
    )

    threats: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    summary: str