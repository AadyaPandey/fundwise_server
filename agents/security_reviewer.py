from graph.state import GrantState

from models.security_models import (
    SecurityReview,
    SecurityScanResult,
)
from security.gemini_analyzer import analyze_application
from security.scanner import scan_application


def security_reviewer_agent(state: GrantState):

    print("\n===== Security Reviewer =====")

    application = state["application"]

    # ----------------------------
    # Rule-based scan
    # ----------------------------

    scan_result: SecurityScanResult = scan_application(application)

    threats = []
    warnings = []
    recommendations = []

    if scan_result.injection:
        threats.extend(
            [
                f"Prompt injection detected: '{p}'"
                for p in scan_result.injection
            ]
        )

    if scan_result.policy_bypass:
        threats.extend(
            [
                f"Policy bypass attempt: '{p}'"
                for p in scan_result.policy_bypass
            ]
        )

    if scan_result.suspicious:
        warnings.extend(
            [
                f"Suspicious instruction: '{p}'"
                for p in scan_result.suspicious
            ]
        )

    # ---------------------------------
    # High-confidence attack
    # ---------------------------------

    if scan_result.has_threats:

        review = SecurityReview(
            safe=False,

            injection_detected=bool(scan_result.injection),

            policy_bypass_detected=bool(
                scan_result.policy_bypass
            ),

            suspicious_instructions=bool(
                scan_result.suspicious
            ),

            security_score=20,

            threats=threats,

            warnings=warnings,

            recommendations=[
                "Escalate to manual review.",
                "Ignore embedded AI instructions.",
            ],

            summary="Security threats detected by rule-based scanner."
        )

        state["security_review"] = review

        return state

    # ---------------------------------
    # Gemini will be added here
    # ---------------------------------


    gemini_result = analyze_application(application)

    review = SecurityReview(
        safe=gemini_result.safe,

        injection_detected=False,
        policy_bypass_detected=False,
        suspicious_instructions=False,

        security_score=gemini_result.security_score,

        threats=gemini_result.threats,

        warnings=gemini_result.warnings,

        recommendations=gemini_result.recommendations,

        summary=gemini_result.summary,
    )

    state["security_review"] = review

    return state