from models.application import GrantApplication
from models.security_models import SecurityScanResult

from security.patterns import (
    PROMPT_INJECTION_PATTERNS,
    POLICY_BYPASS_PATTERNS,
    SUSPICIOUS_PATTERNS,
)


def scan_application(
    application: dict,
) -> SecurityScanResult:
    """
    Deterministically scan a grant application for
    prompt injection, policy bypass, and suspicious
    instructions.
    """

    if hasattr(application, "model_dump"):
        values = application.model_dump().values()
    else:
        values = application.values()

    application_text = " ".join(
        str(value)
        for value in application.values()
        if value is not None
    ).lower()

    result = SecurityScanResult()

    # -----------------------------
    # Prompt Injection
    # -----------------------------

    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in application_text:
            result.injection.append(pattern)

    # -----------------------------
    # Policy Bypass
    # -----------------------------

    for pattern in POLICY_BYPASS_PATTERNS:
        if pattern in application_text:
            result.policy_bypass.append(pattern)

    # -----------------------------
    # Suspicious Instructions
    # -----------------------------

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in application_text:
            result.suspicious.append(pattern)

    return result