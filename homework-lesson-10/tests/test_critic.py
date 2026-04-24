from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

critique_quality = GEval(
    name="Critique Quality",
    evaluation_steps=[
        "Check that the critique identifies specific issues, not vague complaints",
        "Check that revision_requests are actionable (researcher can act on them)",
        "If verdict is APPROVE, gaps list should be empty or contain only minor items",
        "If verdict is REVISE, there must be at least one revision_request",
    ],
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    model="gpt-5.4-mini",
    threshold=0.7,
)

# тут хардом прописати для критика якийсь поганий звіт
# і взяти з прикладів в аутпуті хороший 

def test_critique_approve():
    pass

def test_critique_revise():
    pass