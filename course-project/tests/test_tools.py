from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import ToolCorrectnessMetric
from deepeval import assert_test
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner import planner
from agents.coder import coder
from agents.reviewer import reviewer
from helper import get_unique_tool_names
from config import LLM_test

tool_correctness_metric = ToolCorrectnessMetric(threshold=0.7, model=LLM_test)

def test_planner_tools():
    user_input = """
    We need a report showing the top 10 best-selling products by total revenue in the last fiscal year. 
    Create a technical specification for this SQL query, including the necessary tables and joins.
    """
    agent_response = planner.invoke(
        {"messages": [("user", user_input)]}, 
        config={"configurable": {"thread_id": "test_planner_001"}}
    )

    unique_tool_names = get_unique_tool_names(agent_response)

    test_case = LLMTestCase(
        input=user_input,
        actual_output="Spec ready",
        tools_called=[ToolCall(name=tool_name) for tool_name in unique_tool_names],
        expected_tools=[
            ToolCall(name="list_schemas_and_tables"),
            ToolCall(name="knowledge_search"),
            ToolCall(name="get_table_structure"),
            ToolCall(name="get_sample_rows")
        ],
    )
    assert_test(test_case, [tool_correctness_metric])

def test_planner_tools_error_request():
    user_input = """
    kjdhfishd jhdfjh ksjdjj NOW!!!!.
    """
    agent_response = planner.invoke(
        {"messages": [("user", user_input)]}, 
        config={"configurable": {"thread_id": "test_planner_002"}}
    )

    unique_tool_names = get_unique_tool_names(agent_response)

    test_case = LLMTestCase(
        input=user_input,
        actual_output="Spec ready",
        tools_called=[ToolCall(name=tool_name) for tool_name in unique_tool_names],
        expected_tools=[
            ToolCall(name="ask_user_for_clarification")
        ],
    )
    assert_test(test_case, [tool_correctness_metric])

def test_coder_tools():
    user_input = """
    Based on the approved spec, write a T-SQL query for the AdventureWorks DWH.
    Requirements:
    - Tables: Sales.SalesOrderDetail, Production.Product
    - Logic: Join them on ProductID, sum LineTotal as TotalRevenue.
    - Output: ProductName, TotalRevenue. Group by ProductName, Order by TotalRevenue DESC, limit to Top 10.
    """
    agent_response = coder.invoke(
        {"messages": [("user", {"thread_id": "test_coder_001"})]}, 
        config=config
    )

    unique_tool_names = get_unique_tool_names(agent_response)

    test_case = LLMTestCase(
        input=user_input,
        actual_output="Code ready",
        tools_called=[ToolCall(name=tool_name) for tool_name in unique_tool_names],
        expected_tools=[
            ToolCall(name="get_table_structure"),
            ToolCall(name="execute_sql_query"),
            ToolCall(name="get_sql_execution_plan")
        ],
    )
    assert_test(test_case, [tool_correctness_metric])

def test_reviewer_tools():
    sql_to_review = """
    SELECT TOP 10 p.Name AS ProductName, SUM(sod.LineTotal) AS TotalRevenue
    FROM Sales.SalesOrderDetail sod
    INNER JOIN Production.Product p ON sod.ProductID = p.ProductID
    GROUP BY p.Name
    ORDER BY TotalRevenue DESC;
    """
    user_input = f"Please review the following SQL query for accuracy and performance against the database:\n\n{sql_to_review}"
    agent_response = reviewer.invoke(
        {"messages": [("user", user_input)]}, 
        config={"configurable": {"thread_id": "test_reviewer_001"}}
    )

    unique_tool_names = get_unique_tool_names(agent_response)

    test_case = LLMTestCase(
        input=user_input,
        actual_output="Review ready",
        tools_called=[ToolCall(name=tool_name) for tool_name in unique_tool_names],
        expected_tools=[
            ToolCall(name="execute_sql_query"),
            ToolCall(name="get_sql_execution_plan")
        ],
    )
    assert_test(test_case, [tool_correctness_metric])

    # deepeval test run tests/test_tools.py