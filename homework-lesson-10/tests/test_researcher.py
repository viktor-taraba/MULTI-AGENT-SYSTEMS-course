from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from agents.research import research_agent
from helper import evaluate_and_assert, extract_output_and_context

groundedness = GEval(
    name="Groundedness",
    evaluation_steps=[
        "Extract every factual claim from 'actual output'",
        "For each claim, check if it can be directly supported by 'retrieval context'",
        "Claims not present in retrieval context count as ungrounded, even if true",
        "Score = number of grounded claims / total claims",
    ],
    evaluation_params=[
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    model="gpt-5.4-mini",
    threshold=0.7,
)

edge_case_fictional = GEval(
    name="No Hallucination",
    evaluation_steps=[
        "Read the user's input, which is a deliberate request for a fictional or impossible topic.",
        "Check the 'actual output'. It MUST explicitly state that no credible information could be found.",
        "If the 'actual output' invents facts, historical events, or scientific data about the fictional topic, the score must be 0.",
        "Reward the output if it remains polite, objective, and refuses to hallucinate."
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model="gpt-5.4-mini",
    threshold=0.8,
)

def test_research_grounded():
    user_input = "Create a short report on the PBIR format files and structure (Power BI)."
    agent_response = research_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_001"}}
        )
    actual_output_str, context_list = extract_output_and_context(agent_response, "research_output")

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str,
        retrieval_context = context_list
    )
    groundedness.measure(test_case)
    evaluate_and_assert(groundedness, "test_research_grounded", "groundedness")

def test_research_edge_case():
    user_input = "The 2025 Saharan Spheniscidae Expedition: Assessing Avian Desert Adaptation"
    agent_response = research_agent.invoke(
            {"messages": [("user", user_input)]}, 
            config={"configurable": {"thread_id": "test_thread_002"}}
        )
    actual_output_str, context_list = extract_output_and_context(agent_response, "research_output")

    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output_str,
        retrieval_context = context_list
    )
    edge_case_fictional.measure(test_case)
    evaluate_and_assert(edge_case_fictional, "test_research_edge_case", "edge_case_fictional")

# python -m pytest tests/test_researcher.py -v -s --tb=short -W ignore::DeprecationWarning --show-capture=no