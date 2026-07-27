from graph.state import GrantState

from models.judge_models import (
    Decision,
    GrantDecision,
)


def judge_agent(state: GrantState):

    print("\n===== Judge Agent =====")

    review = state["review"]
    security = state["security_review"]
    tool_results = state["tool_results"]

    reasons = []
    recommendations = []

    # ---------------------------------
    # Security Check
    # ---------------------------------

    if not security.safe:

        reasons.append(
            "Security threats detected in the application."
        )

        state["final_decision"] = GrantDecision(
            decision=Decision.REJECT,
            confidence=100,
            reasons=reasons,
            recommendations=[
                "Escalate to manual investigation."
            ],
            summary="Application rejected due to security risks."
        )

        return state

    # ---------------------------------
    # Registration Check
    # ---------------------------------

    registration = tool_results.get("registration")

    if registration and not registration.data.get("valid", False):

        reasons.append(
            "NGO registration is invalid."
        )

        state["final_decision"] = GrantDecision(
            decision=Decision.REJECT,
            confidence=95,
            reasons=reasons,
            recommendations=[
                "Verify NGO registration details."
            ],
            summary="Application rejected due to invalid registration."
        )

        return state

    # ---------------------------------
    # Documentation Check
    # ---------------------------------

    documentation = tool_results.get("documentation")

    if documentation and not documentation.data.get("complete", False):

        reasons.append(
            "Required supporting documents are missing."
        )

        state["final_decision"] = GrantDecision(
            decision=Decision.MANUAL_REVIEW,
            confidence=90,
            reasons=reasons,
            recommendations=[
                "Submit the missing supporting documents."
            ],
            summary="Manual review required due to incomplete documentation."
        )

        return state

    # ---------------------------------
    # Eligibility Check
    # ---------------------------------

    eligibility = tool_results.get("eligibility")

    if eligibility and not eligibility.data.get("eligible", False):

        reasons.append(
            "The applicant does not satisfy the eligibility criteria."
        )

        state["final_decision"] = GrantDecision(
            decision=Decision.REJECT,
            confidence=90,
            reasons=reasons,
            recommendations=[
                "Review the eligibility requirements."
            ],
            summary="Application rejected due to eligibility."
        )

        return state

    # ---------------------------------
    # Budget Check
    # ---------------------------------

    budget = tool_results.get("budget")

    if budget and not budget.data.get("within_limit", False):

        reasons.append(
            "Budget validation failed."
        )

        state["final_decision"] = GrantDecision(
            decision=Decision.MANUAL_REVIEW,
            confidence=90,
            reasons=reasons,
            recommendations=[
                "Revise the submitted budget."
            ],
            summary="Budget requires manual review."
        )

        return state

    # ---------------------------------
    # Policy Compliance Check
    # ---------------------------------



    # policy = tool_results.get("policy_rag")

    # if policy:

    #     overall_status = policy.data.get("overall_status")

    #     if overall_status == "NON_COMPLIANT":

    #         reasons.append(
    #             "Application violates one or more organizational funding policies."
    #         )

    #         findings = policy.data.get("findings", [])

    #         for finding in findings:
    #             reasons.append(
    #                 f"{finding['policy_name']}: {finding['explanation']}"
    #             )

    #         state["final_decision"] = GrantDecision(
    #             decision=Decision.REJECT,
    #             confidence=95,
    #             reasons=reasons,
    #             recommendations=[
    #                 "Resolve all policy violations before resubmission."
    #             ],
    #             summary="Application rejected due to policy violations."
    #         )

    #         return state

    #     elif overall_status == "NEEDS_REVIEW":

    #         reasons.append(
    #             "Application requires manual review due to policy observations."
    #         )

    #         findings = policy.data.get("findings", [])

    #         for finding in findings:
    #             reasons.append(
    #                 f"{finding['policy_name']}: {finding['explanation']}"
    #             )

    #         state["final_decision"] = GrantDecision(
    #             decision=Decision.MANUAL_REVIEW,
    #             confidence=90,
    #             reasons=reasons,
    #             recommendations=[
    #                 "Review the policy compliance findings."
    #             ],
    #             summary="Manual review required due to policy findings."
    #         )

    #         return state

    # ---------------------------------
    # Quality Check
    # ---------------------------------

    if review.coverage_score < 80:

        reasons.append(
            "Tool execution coverage is too low."
        )

        state["final_decision"] = GrantDecision(
            decision=Decision.MANUAL_REVIEW,
            confidence=80,
            reasons=reasons,
            recommendations=[
                "Complete pending tool executions."
            ],
            summary="Manual review recommended."
        )

        return state

    # ---------------------------------
    # Everything Passed
    # ---------------------------------

    state["final_decision"] = GrantDecision(
        decision=Decision.APPROVE,
        confidence=95,
        reasons=[
            "Application passed all automated verification checks."
        ],
        recommendations=[],
        summary="Application approved."
    )

    return state