from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval, AnswerRelevancyMetric, ToxicityMetric
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
import json 
from collections import defaultdict

relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-5.4-mini")

toxicity = ToxicityMetric(threshold=0.8, model="gpt-5.4-mini")

correctness = GEval(
    name="Correctness",
    evaluation_steps=[
        "Check whether the facts in 'actual output' contradict any facts in 'expected output'",
        "Penalize omission of critical details",
        "Different wording of the same concept is acceptable",
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model="gpt-5.4-mini",
    threshold=0.6,
)

conciseness = GEval(
    name="Conciseness",
    evaluation_steps=[
        "Check if the 'actual output' directly answers the 'input' without unnecessary filler.",
        "Penalize conversational fluff (e.g., 'Sure, here is your answer:').",
        "Penalize repetition of the same points.",
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model="gpt-5.4-mini",
    threshold=0.7,
)

def test_e2e():
    with open("tests/e2e_results/generated_responses.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = []
    for item in data:
        tc = LLMTestCase(
            input=item["input"],
            actual_output=item["actual_output"],
            expected_output=item["expected_output"],
        )
        test_cases.append(tc)

    dataset = EvaluationDataset()
    for tc in test_cases:
        dataset.add_test_case(tc)

    results = evaluate(
        test_cases=dataset.test_cases,
        metrics=[correctness, relevancy, toxicity, conciseness]
    )

# test_e2e()

# python -m tests.test_e2e
# deepeval test run test_e2e.py