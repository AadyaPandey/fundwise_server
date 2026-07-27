from typing import Any, Literal
from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """
    Standard response format for every tool in GrantGuard.
    """

    tool: str = Field(
        description="Name of the tool that generated this result."
    )

    status: Literal[
        "SUCCESS",
        "FAILED",
        "NOT_IMPLEMENTED",
    ] = Field(
        description="Execution status of the tool."
    )

    success: bool = Field(
        description="Whether the tool executed successfully."
    )

    reason: str = Field(
        description="Human-readable explanation of the result."
    )

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured output produced by the tool."
    )