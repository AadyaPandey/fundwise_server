from models.tool_models import ToolResult


REQUIRED_REGISTRATION_DOCUMENT = "Registration Certificate"


def registration_tool(application: dict) -> ToolResult:
    """
    Verify NGO registration details.
    """

    registration_number = application.get("registration_number")

    try:
        years_operating = int(
            application.get("years_operating", 0)
        )
    except (TypeError, ValueError):
        return ToolResult(
            tool="registration",
            status="FAILED",
            success=False,
            reason="Invalid years operating value.",
            data={
                "valid": False,
                "registration_number": registration_number,
                "certificate_found": False,
                "issues": [
                    "Years operating must be a valid number."
                ],
            },
        )

    documents = application.get("documents", [])

    if not isinstance(documents, list):
        return ToolResult(
            tool="registration",
            status="FAILED",
            success=False,
            reason="Invalid documents format.",
            data={
                "valid": False,
                "registration_number": registration_number,
                "certificate_found": False,
                "issues": [
                    "Documents must be provided as a list."
                ],
            },
        )

    certificate_found = (
        REQUIRED_REGISTRATION_DOCUMENT in documents
    )

    valid = (
        bool(registration_number)
        and years_operating > 0
        and certificate_found
    )

    issues = []

    if not registration_number:
        issues.append(
            "Registration number is missing."
        )

    if years_operating <= 0:
        issues.append(
            "Invalid years operating."
        )

    if not certificate_found:
        issues.append(
            "Registration Certificate not submitted."
        )

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