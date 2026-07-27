from tools.registration import registration_tool
from tools.budget import budget_tool
from tools.eligibility import eligibility_tool
from tools.documentation import documentation_tool
from graph.state import GrantState
from models.tool_models import ToolResult
# from tools.policy_rag import policy_rag_tool

# TOOLS = {
#     "registration": registration_tool,
#     "budget": budget_tool,
#     "eligibility": eligibility_tool,
# }


# def worker_agent(state: GrantState):
#     print("\n===== Worker Agent =====")
#     application = state["application"]

#     results = {}

#     for step in state["plan"].steps:

#         tool_name = step.tool

#         if tool_name not in TOOLS:
#             results[tool_name] = ToolResult(
#                 tool=tool_name,
#                 status="NOT_IMPLEMENTED",
#                 success=False,
#                 reason=f"{tool_name} tool has not been implemented yet.",
#                 data={}
#             )
#             continue

#         tool = TOOLS[tool_name]

#         results[tool_name] = tool(application)

#     state["tool_results"] = results

#     return state



from concurrent.futures import ThreadPoolExecutor, as_completed

TOOLS = {
    "registration": registration_tool,
    "budget": budget_tool,
    "eligibility": eligibility_tool,
    # "policy_rag": policy_rag_tool,
    "documentation": documentation_tool,
}


def run_tool(step, application):
    tool_name = step.tool

    if tool_name not in TOOLS:
        return (
            tool_name,
            ToolResult(
                tool=tool_name,
                status="NOT_IMPLEMENTED",
                success=False,
                reason=f"{tool_name} tool has not been implemented yet.",
                data={}
            )
        )

    tool = TOOLS[tool_name]
    return tool_name, tool(application)


def worker_agent(state: GrantState):
    print("\n===== Worker Agent =====")

    application = state["application"]
    results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(run_tool, step, application)
            for step in state["plan"].steps
        ]

        for future in as_completed(futures):
            tool_name, result = future.result()
            results[tool_name] = result

    state["tool_results"] = results
    return state