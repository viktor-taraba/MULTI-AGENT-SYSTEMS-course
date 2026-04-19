from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
#import os, sys
# Add the parent directory (project root) to the system path
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner import planner_agent
from deepeval import assert_test
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
    threshold=0.99,
)

def test_plan_quality():
    user_input = "Create a detailed research plan on the effects of microplastics on marine ecosystems."

    config = {"configurable": {"thread_id": "test_thread_001"}}
    agent_response = planner_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config=config
        )

    if hasattr(agent_response, "model_dump_json"):
        actual_output_str = agent_response.model_dump_json()
    else:
        actual_output_str = str(agent_response)

    #print(actual_output_str)

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str
    )
    plan_quality.measure(test_case)

    if plan_quality.is_successful():
        print(f"\n✅ test_plan_quality ({plan_quality.name}: {plan_quality.score}, threshold: {plan_quality.threshold})")
    else:
        print(f"\n❌ test_plan_quality ({plan_quality.name}: {plan_quality.score}, threshold: {plan_quality.threshold})")
        print(f"   Reason: {plan_quality.reason}")
            
        pytest.fail("DeepEval threshold not met.")

#def test_plan_has_queries():
 #   pass

#print(test_plan_quality())

# python -m pytest tests/test_planner.py -v -s --tb=short -W ignore::DeprecationWarning