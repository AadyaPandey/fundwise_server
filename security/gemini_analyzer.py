from dataclasses import dataclass
from typing import List

from llm import llm
from models.security_models import GeminiSecurityAnalysis
from security.prompts import SECURITY_REVIEW_PROMPT

structured_llm = llm.with_structured_output(
    GeminiSecurityAnalysis
)

@dataclass
class GeminiSecurityResult:
    safe: bool
    security_score: int
    threats: List[str]
    warnings: List[str]
    recommendations: List[str]
    summary: str


def analyze_application(application: dict) -> GeminiSecurityResult:
    """
    Analyze the grant application for prompt injection,
    policy manipulation, jailbreak attempts, and other
    suspicious instructions using Gemini.

    Placeholder implementation.
    """

    return GeminiSecurityResult(
        safe=True,
        security_score=100,
        threats=[],
        warnings=[],
        recommendations=[],
        summary="Gemini analysis not implemented yet."
    )

def analyze_application(application: dict) -> GeminiSecurityAnalysis:
    """
    Analyze a grant application for prompt injection,
    policy bypass attempts, and suspicious instructions.
    """

    prompt = SECURITY_REVIEW_PROMPT.format(
        application=application
    )

    try:
        return structured_llm.invoke(prompt)

    except Exception:
        return GeminiSecurityAnalysis(
            safe=True,
            injection_detected=False,
            policy_bypass_detected=False,
            suspicious_instructions=False,
            security_score=50,
            threats=[],
            warnings=[
                "Gemini security analysis could not be completed."
            ],
            recommendations=[
                "Review manually if security is critical."
            ],
            summary="Gemini analysis failed."
        )