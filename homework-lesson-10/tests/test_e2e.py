from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval import evaluate

dataset = EvaluationDataset()
for tc in test_cases:
    dataset.add_test_case(tc)
print(f"\nGolden Dataset created: {len(dataset.test_cases)} test cases")
print("\nThis dataset can be saved and versioned for regression testing")

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

relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-5.4-mini")

print("Running full evaluation on Golden Dataset...")
results = evaluate(
    test_cases=dataset.test_cases,
    metrics=[correctness, relevancy],
)

# python -m tests.test_e2e