from langgraph.graph import StateGraph, START, END

from graph.state import GrantState
from agents.planner import planner_agent
from agents.worker import worker_agent
from agents.reviewer import reviewer_agent
from agents.security_reviewer import security_reviewer_agent
from agents.judge import judge_agent

builder = StateGraph(GrantState)

# Add nodes
builder.add_node("planner", planner_agent)

# Planner Node
#       │
#       ▼
# planner_agent(state)

builder.add_node("worker", worker_agent)

# Planner
#   ↓
# Worker

builder.add_node("reviewer", reviewer_agent)

builder.add_node("security_reviewer", security_reviewer_agent)

builder.add_node("judge", judge_agent)

# Define execution flow
builder.add_edge(START, "planner")
builder.add_edge("planner", "worker")
builder.add_edge("worker", "reviewer")
#comment and uncomment the below line to skip security review
builder.add_edge("reviewer", "security_reviewer")
builder.add_edge("security_reviewer", "judge")
builder.add_edge("judge", END)
# builder.add_edge("reviewer", END)
#ADD TESTS
graph = builder.compile()