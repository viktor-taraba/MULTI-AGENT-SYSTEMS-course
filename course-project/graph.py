from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command, interrupt
from typing import Literal
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from config import to_save_graph_image
from langgraph.checkpoint.memory import InMemorySaver

# Reviewer routing: return string, not Command (conditional edges require strings)
def review_router(state: MessagesState) -> Literal["coder", "__end__"]:
    """Route based on reviewer verdict."""
    last_msg = state["messages"][-1].content
    if "APPROVED" in last_msg.upper():
        return END
    return "coder"

def human_approval_gate(state: MessagesState) -> Command[Literal["coder", "planner"]]:
    """Human-in-the-Loop (HITL) gate for BA to review the spec."""

    feedback = interrupt("Please review the Planner's Output. Type 'APPROVED' to accept, or provide feedback about what to change.")
    if feedback.strip().upper() == "APPROVED":
        return Command(goto="coder")
    else:
        return Command(
            goto="planner",
            update={"messages": [("user", f"Spec rejected by the User. Feedback: {feedback}")]}
        )

# Build the graph: planner → HITL → coder → reviewer → (loop or end)
graph = StateGraph(MessagesState)

graph.add_node("planner", planner)
graph.add_node("human_approval_gate", human_approval_gate)
graph.add_node("coder", coder)
graph.add_node("reviewer", reviewer)

graph.add_edge(START, "planner")
graph.add_edge("planner", "human_approval_gate")
graph.add_edge("coder", "reviewer")
graph.add_conditional_edges("reviewer", review_router)

memory = InMemorySaver()
dev_team_app = graph.compile(checkpointer=memory)

if to_save_graph_image == 1:
    try:
        graph_image = dev_team_app.get_graph().draw_mermaid_png()
        with open("graph_structure.png", "wb") as f:
            f.write(graph_image)
        print("Graph image successfully saved to 'graph_structure.png'")
        
    except Exception as e:
        print(f"Failed to generate graph image: {e}")