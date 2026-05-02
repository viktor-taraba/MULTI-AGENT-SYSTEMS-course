from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command, Interrupt
from typing import Literal
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer

# Reviewer routing: return string, not Command (conditional edges require strings)
def review_router(state: MessagesState) -> Literal["coder", "__end__"]:
    """Route based on reviewer verdict."""
    last_msg = state["messages"][-1].content
    if "APPROVED" in last_msg.upper():
        return END
    return "coder"

# Build the graph: planner → coder → reviewer → (loop or end)
graph = StateGraph(MessagesState)
graph.add_node("planner", planner)
graph.add_node("coder", coder)
graph.add_node("reviewer", reviewer)
graph.add_edge(START, "planner")
graph.add_edge("planner", "coder")
graph.add_edge("coder", "reviewer")
graph.add_conditional_edges("reviewer", review_router)

dev_team_app = graph.compile()