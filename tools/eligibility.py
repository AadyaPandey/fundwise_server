from models.tool_models import ToolResult


SUPPORTED_CATEGORIES = {
    "Healthcare",
    "Education",
    "Environment",
    "Women Empowerment",
    "Child Welfare",
    "Livelihood",
}

MIN_YEARS_OPERATING = 3
MIN_BENEFICIARIES = 100
MAX_REQUESTED_AMOUNT = 2_000_000


def eligibility_tool(application: dict) -> ToolResult:
    """
    Evaluate whether the NGO is eligible for grant consideration.
    """

    try:
        years_operating = int(
            application.get("years_operating", 0)
        )

        beneficiaries = int(
            application.get("beneficiaries", 0)
        )

        grant_category = application.get(
            "grant_category", ""
        )

        requested_amount = float(
            application.get("requested_amount", 0)
        )

    except (TypeError, ValueError) as e:
        return ToolResult(
            tool="eligibility",
            status="FAILED",
            success=False,
            reason=f"Invalid application data: {str(e)}",
            data={
                "eligible": False,
                "issues": [
                    "One or more eligibility fields contain invalid values."
                ],
            },
        )

    issues = []

    if years_operating < MIN_YEARS_OPERATING:
        issues.append(
            f"NGO must have at least "
            f"{MIN_YEARS_OPERATING} years of operation."
        )

    if beneficiaries < MIN_BENEFICIARIES:
        issues.append(
            f"Project must benefit at least "
            f"{MIN_BENEFICIARIES} beneficiaries."
        )

    if grant_category not in SUPPORTED_CATEGORIES:
        issues.append(
            f"Grant category '{grant_category}' "
            f"is not supported."
        )

    if requested_amount > MAX_REQUESTED_AMOUNT:
        issues.append(
            f"Requested amount exceeds the maximum allowed "
            f"limit of ₹{MAX_REQUESTED_AMOUNT:,}."
        )

    eligible = len(issues) == 0

    return ToolResult(
        tool="eligibility",
        status="SUCCESS",
        success=True,
        reason="Eligibility evaluation completed.",
        data={
            "eligible": eligible,
            "grant_category": grant_category,
            "years_operating": years_operating,
            "beneficiaries": beneficiaries,
            "requested_amount": requested_amount,
            "issues": issues,
        },
    )