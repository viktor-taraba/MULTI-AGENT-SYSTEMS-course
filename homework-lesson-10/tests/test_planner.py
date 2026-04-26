from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from agents.planner import planner_agent
from helper import evaluate_and_assert

plan_quality = GEval(
    name="Plan Quality",
    evaluation_steps=[
        "Check that the plan contains specific search queries (not vague)",
        "Check that sources_to_check includes relevant sources for the topic",
        "Check that the output_format matches what the user asked for",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.7,
)

plan_has_queries = GEval(
    name="Plan Has Queries",
    evaluation_steps=[
        "Check that the output explicitly lists one or more actionable search queries in the `search_queries`.",
        "Check that the queries are highly relevant to the user's prompt.",
        "Check that either tool `web_search` or `knowledge_search` was recommended at least 2 times in the `sources_to_check` with relevant parameters"
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.8,
)

plan_query_diversity = GEval(
    name="Query Diversity",
    evaluation_steps=[
        "Extract the 'search_queries' list from the output.",
        "Compare the queries against each other to check for redundancy and overlapping intent.",
        "Score highly if the queries are distinct and offer broad coverage of the topic. Score poorly if they are practically synonymous."
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.75,
)

def test_plan_quality():
    user_input = "Create a detailed research plan on the effects of microplastics on marine ecosystems."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_quality.measure(test_case)
    evaluate_and_assert(plan_quality, "test_plan_quality", "plan_quality")

def test_plan_has_queries():
    user_input = "Create a detailed research plan on the dividend policy types."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_002"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_has_queries.measure(test_case)
    evaluate_and_assert(plan_quality, "test_plan_has_queries", "plan_has_queries")

def test_query_diversity():
    user_input = "Create a detailed research plan on the PBIR format files and structure (Power BI)."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_003"}}
        )
    actual_output_str = str(agent_response.get("messages", [])[-1].content)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_query_diversity.measure(test_case)
    evaluate_and_assert(plan_query_diversity, "test_query_diversity", "plan_query_diversity")

# python -m pytest tests/test_planner.py -v -s --tb=short -W ignore::DeprecationWarning --no-header