from llm import llm
from prompts.planner_prompt import PLANNER_PROMPT
from graph.state import GrantState
from models.planner_models import ExecutionPlan

structured_llm = llm.with_structured_output(ExecutionPlan)


def planner_agent(state: GrantState):
    print("\n===== Planner Agent =====")
    application = state["application"]

    prompt = f"""
{PLANNER_PROMPT}

Application:

{application}
"""

    plan = structured_llm.invoke(prompt)

    state["plan"] = plan

    return state