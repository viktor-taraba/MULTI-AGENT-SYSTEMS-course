from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command, interrupt
from langgraph.graph.message import add_messages
from typing import Annotated, Literal
from typing_extensions import TypedDict
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from config import to_save_graph_image
from langgraph.checkpoint.memory import InMemorySaver

class DevTeamState(TypedDict):
    messages: Annotated[list, add_messages]
    iteration: int

def reviewer_node(state: DevTeamState) -> Command[Literal["coder", "__end__"]]:
    """Runs the reviewer and routes dynamically using the Command API."""
    
    current_iteration = state.get("iteration", 0)
    reviewer_response = reviewer.invoke(state) 
    last_msg = reviewer_response["messages"][-1].content
    
    if "APPROVED" in last_msg.upper() or current_iteration >= 5:
        return Command(
            goto=END,
            update={
                "messages": reviewer_response["messages"],
                "iteration": current_iteration + 1
            })
    else:
        payload = f"Revision Needed. Fix the following based on QA feedback:\n{last_msg}"
        return Command(
            goto="coder",
            update={
                "messages": [("user", payload)], 
                "iteration": current_iteration + 1
            })

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