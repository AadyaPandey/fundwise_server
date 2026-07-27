from models.tool_models import ToolResult


REQUIRED_DOCUMENTS = {
    "Registration Certificate",
    "PAN Card",
    "Audited Financial Statements (Last 3 Years)",
    "Bank Statement (Last 6 Months)",
    "Project Timeline",
    "Board Resolution",
}


def documentation_tool(application: dict) -> ToolResult:
    """
    Verify that all mandatory supporting documents have been submitted.
    """

    submitted_documents = set(application.get("documents", []))

    missing_documents = sorted(
        REQUIRED_DOCUMENTS - submitted_documents
    )

    complete = len(missing_documents) == 0

    return ToolResult(
        tool="documentation",
        status="SUCCESS",
        success=True,
        reason="Documentation verification completed.",
        data={
            "complete": complete,
            "submitted_documents": sorted(submitted_documents),
            "required_documents": sorted(REQUIRED_DOCUMENTS),
            "missing_documents": missing_documents,
            "missing_count": len(missing_documents),
        },
    )