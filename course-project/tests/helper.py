from langgraph.graph import StateGraph, MessagesState, START, END
from typing import Literal
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import recursion_limit
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer

# function for running graph + simplified graph (without HITL) for e2e testing

# Reviewer routing: return string, not Command (conditional edges require strings)
def review_router(state: MessagesState) -> Literal["coder", "__end__"]:
    """Route based on reviewer verdict."""
    last_msg = state["messages"][-1].content
    if "APPROVED" in last_msg.upper():
        return END
    return "coder"

# Build the graph: planner → HITL → coder → reviewer → (loop or end)
graph_e2e_test = StateGraph(MessagesState)
graph_e2e_test.add_node("planner", planner)
graph_e2e_test.add_node("coder", coder)
graph_e2e_test.add_node("reviewer", reviewer)
graph_e2e_test.add_edge(START, "planner")
graph_e2e_test.add_edge("planner", "coder")
graph_e2e_test.add_edge("coder", "reviewer")
graph_e2e_test.add_conditional_edges("reviewer", review_router)

dev_team_app_e2e_test = graph_e2e_test.compile()

def run_e2e_graph(user_input: str, thread_id: str) -> str:
    """Helper function to execute the full LangGraph and extract the final code for e2e tests."""

    inputs = {"messages": [("user", user_input)]}
    config = {"recursion_limit": recursion_limit, "configurable": {"thread_id": thread_id}}
    final_state = dev_team_app_e2e_test.invoke(inputs, config=config)
    
    # to delete
    print(str(final_state["messages"]))

    for message in reversed(final_state["messages"]):
        content_str = str(message.content)
        
        if "source_code" in content_str and "description" in content_str:
            return content_str
            
    return str(final_state["messages"].content)

user_input = """
Title: Most Recently Hired Employee per Department
Requirements: Find the newest, currently active employee in each department. You must join HumanResources.Employee, HumanResources.EmployeeDepartmentHistory, HumanResources.Department, and Person.Person to get the actual names. 
Acceptance Criteria:
- Must return DepartmentName, FirstName, LastName, and HireDate.
- Must filter EmployeeDepartmentHistory to only include current assignments (where EndDate IS NULL).
- Must use a window function (like ROW_NUMBER) to partition by department and sort by HireDate descending.
"""
actual_output_str = run_e2e_graph(user_input, "e2e_001")
print(actual_output_str)