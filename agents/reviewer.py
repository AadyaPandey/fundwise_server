from graph.state import GrantState
from models.review_models import QualityReview


def reviewer_agent(state: GrantState):

    print("\n===== Quality Reviewer =====")

    plan = state["plan"]
    tool_results = state["tool_results"]

    missing_required = []
    failed_tools = []

    strengths = []
    weaknesses = []

    required_steps = [
        step
        for step in plan.steps
        if step.required
    ]

    successful_required = 0

    for step in required_steps:

        result = tool_results.get(step.tool)

        if result is None:
            missing_required.append(step.tool)
            weaknesses.append(f"{step.tool} was not executed.")
            continue

        if not result.success:
            failed_tools.append(step.tool)
            weaknesses.append(
                f"{step.tool} failed: {result.reason}"
            )
            continue

        successful_required += 1
        strengths.append(
            f"{step.tool} executed successfully."
        )

    if required_steps:
        coverage = (
            successful_required /
            len(required_steps)
        ) * 100
    else:
        coverage = 100

    evidence_points = 0

    for result in tool_results.values():

        if result.success and result.data:
            evidence_points += 1

    if tool_results:
        evidence_score = (
            evidence_points /
            len(tool_results)
        ) * 100
    else:
        evidence_score = 0

    confidence = (
        coverage * 0.7 +
        evidence_score * 0.3
    )

    review = QualityReview(
        passed=(
            coverage == 100
            and not failed_tools
            and not missing_required
        ),
        coverage_score=round(coverage, 2),
        evidence_score=round(evidence_score, 2),
        confidence_score=round(confidence, 2),
        missing_required_tools=missing_required,
        failed_tools=failed_tools,
        strengths=strengths,
        weaknesses=weaknesses,
        summary=f"{successful_required}/{len(required_steps)} required tools executed successfully."
    )

    state["review"] = review

    return state