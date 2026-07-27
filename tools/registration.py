from models.tool_models import ToolResult


REQUIRED_REGISTRATION_DOCUMENT = "Registration Certificate"


def registration_tool(application: dict) -> ToolResult:
    """
    Verify NGO registration details.
    """

    registration_number = application.get("registration_number")
    years_operating = application.get("years_operating", 0)
    documents = application.get("documents", [])

    certificate_found = REQUIRED_REGISTRATION_DOCUMENT in documents

    valid = (
        bool(registration_number)
        and years_operating > 0
        and certificate_found
    )

    issues = []

    if not registration_number:
        issues.append("Registration number is missing.")

    if years_operating <= 0:
        issues.append("Invalid years operating.")

    if not certificate_found:
        issues.append("Registration Certificate not submitted.")

    return ToolResult(
        tool="registration",
        status="SUCCESS",
        success=True,
        reason="Registration verification completed.",
        data={
            "valid": valid,
            "registration_number": registration_number,
            "years_operating": years_operating,
            "certificate_found": certificate_found,
            "issues": issues,
        },
    )