from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import assert_test
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner import planner as planner_agent
from config import LLM_test

plan_quality = GEval(
    name="Plan Quality",
    evaluation_steps=[
        "Check that the plan contains specific acceptance_criteria (not vague).",
        "Check that requirements list is relevant for the topic and includes at least 2 elements.",
        "Check that the output_format matches what the user asked for.",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

plan_has_queries = GEval(
    name="Plan Has Tables and Joins",
    evaluation_steps=[
        "Check that the output explicitly lists all the specific database tables required to fulfill the user's request.",
        "Check that the output has all the necessary columns needed for selecting data, joining tables, and applying filters.",
        "Check that the output clearly defines the required relationships between tables.",
        "If the query requires summarization, the output explicitly states the necessary mathematical aggregations"
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

plan_edge_cases = GEval(
    name="Edge Case and Data Quality Handling",
    evaluation_steps=[
        "Check if the plan explicitly addresses how to handle potential NULL values in the relevant columns.",
        "Check if the plan explicitly defines tie-handling logic if the query involves sorting, ranking, or finding a 'top'/'max'/'min' record.",
        "Check if the plan mentions handling duplicate records if applicable to the prompt."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7, 
)

plan_alignment = GEval(
    name="Requirements and Criteria Alignment",
    evaluation_steps=[
        "Check that every major logical step defined in the 'requirements' (e.g., a specific join or aggregation) has a corresponding testable condition in the 'acceptance_criteria'.",
        "Check that the 'acceptance_criteria' do NOT introduce new database tables, columns, or business logic that were completely omitted from the 'requirements'."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model=LLM_test,
    threshold=0.7,
)

def test_plan_quality():
    user_input = "Calculate total number of active employees."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [plan_quality])

def test_plan_has_queries():
    user_input = "Total amount of sales by year."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_002"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [plan_has_queries])

def test_plan_edge_cases():
    user_input = "Find the employee with the highest salary in each department."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_003"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [plan_edge_cases])


def test_plan_alignment():
    user_input = "Calculate the month-over-month revenue growth percentage for the last available year."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_004"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    assert_test(test_case, [plan_alignment])

# deepeval test run tests/test_planner.py