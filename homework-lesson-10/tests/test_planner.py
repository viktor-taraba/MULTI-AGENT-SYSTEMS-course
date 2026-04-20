from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
#import os, sys
# Add the parent directory (project root) to the system path
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner import planner_agent
import pytest

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
        "Check that either tool `web_search` or `knowledge_search` was used at least 2 times in the `sources_to_check`"
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
    # загорнути потім у функцію
    user_input = "Create a detailed research plan on the effects of microplastics on marine ecosystems."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )

    if hasattr(agent_response, "model_dump_json"):
        actual_output_str = agent_response.model_dump_json()
    else:
        actual_output_str = str(agent_response)

    # to delete
    print(actual_output_str[:400])

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_quality.measure(test_case)

    # це теж загорнути як окрему ф-ю
    if plan_quality.is_successful():
        print(f"\n✅ test_plan_quality ({plan_quality.name}: {plan_quality.score}, threshold: {plan_quality.threshold})")
    else:
        print(f"\n❌ test_plan_quality ({plan_quality.name}: {plan_quality.score}, threshold: {plan_quality.threshold})")
        print(f"   Reason: {plan_quality.reason}")
        pytest.fail("DeepEval plan_quality threshold not met.")

def test_plan_has_queries():
    # загорнути потім у функцію
    user_input = "Create a detailed research plan on the effects of microplastics on marine ecosystems."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )

    if hasattr(agent_response, "model_dump_json"):
        actual_output_str = agent_response.model_dump_json()
    else:
        actual_output_str = str(agent_response)

    # to delete
    print(actual_output_str[:400])

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_has_queries.measure(test_case)

    if plan_has_queries.is_successful():
        print(f"\n✅ test_plan_has_queries ({plan_has_queries.name}: {plan_has_queries.score}, threshold: {plan_has_queries.threshold})")
    else:
        print(f"\n❌ test_plan_has_queries ({plan_has_queries.name}: {plan_has_queries.score}, threshold: {plan_has_queries.threshold})")
        print(f"   Reason: {plan_has_queries.reason}")
        pytest.fail("DeepEval plan_has_queries threshold not met.")

def test_query_diversity():
    # загорнути потім у функцію
    user_input = "Create a detailed research plan on the effects of microplastics on marine ecosystems."
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )

    if hasattr(agent_response, "model_dump_json"):
        actual_output_str = agent_response.model_dump_json()
    else:
        actual_output_str = str(agent_response)

    # to delete
    print(actual_output_str[:400])

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_query_diversity.measure(test_case)

    # це теж загорнути як окрему ф-ю
    if plan_query_diversity.is_successful():
        print(f"\n✅ test_query_diversity ({plan_query_diversity.name}: {plan_query_diversity.score}, threshold: {plan_query_diversity.threshold})")
    else:
        print(f"\n❌ test_query_diversity ({plan_query_diversity.name}: {plan_query_diversity.score}, threshold: {plan_query_diversity.threshold})")
        print(f"   Reason: {plan_query_diversity.reason}")
        pytest.fail("DeepEval plan_query_diversity threshold not met.")

# python -m pytest tests/test_planner.py -v -s --tb=short -W ignore::DeprecationWarning