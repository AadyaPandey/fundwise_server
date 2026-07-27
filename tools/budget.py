from models.tool_models import ToolResult


MAX_GRANT = 2_000_000
MAX_ADMIN_PERCENTAGE = 20
MAX_CONTINGENCY_PERCENTAGE = 10


def budget_tool(application: dict) -> ToolResult:
    """
    Validate the submitted project budget.
    """

    requested_amount = application.get("requested_amount", 0)
    budget = application.get("budget", {})

    total_budget = sum(budget.values())

    administration = budget.get("administration", 0)
    contingency = budget.get("contingency", 0)

    admin_percentage = (
        (administration / total_budget) * 100
        if total_budget > 0 else 0
    )

    contingency_percentage = (
        (contingency / total_budget) * 100
        if total_budget > 0 else 0
    )

    issues = []

    if requested_amount > MAX_GRANT:
        issues.append(
            f"Requested amount exceeds the maximum grant limit of ₹{MAX_GRANT:,}."
        )

    if total_budget != requested_amount:
        issues.append(
            "Budget breakdown does not match the requested amount."
        )

    if admin_percentage > MAX_ADMIN_PERCENTAGE:
        issues.append(
            f"Administration expenses exceed {MAX_ADMIN_PERCENTAGE}% of the total budget."
        )

    if contingency_percentage > MAX_CONTINGENCY_PERCENTAGE:
        issues.append(
            f"Contingency allocation exceeds {MAX_CONTINGENCY_PERCENTAGE}% of the total budget."
        )

    if any(value < 0 for value in budget.values()):
        issues.append(
            "Budget contains negative values."
        )

    within_limit = len(issues) == 0

    return ToolResult(
        tool="budget",
        status="SUCCESS",
        success=True,
        reason="Budget evaluation completed.",
        data={
            "within_limit": within_limit,
            "requested_amount": requested_amount,
            "budget_total": total_budget,
            "max_grant": MAX_GRANT,
            "administration_percentage": round(admin_percentage, 2),
            "contingency_percentage": round(contingency_percentage, 2),
            "issues": issues,
        },
    )