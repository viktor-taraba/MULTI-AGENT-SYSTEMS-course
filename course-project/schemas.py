from pydantic import BaseModel, Field
from typing import List, Literal

class SpecOutput(BaseModel):
    title: str = Field(description="A concise, descriptive name for the problem being planned.")
    requirements: list[str] = Field(description="A detailed list of logical requirements for the query, including specific tables, columns, joins, filtering conditions (WHERE/HAVING), and aggregations (GROUP BY) needed.")
    acceptance_criteria: list[str] = Field(description="Testable conditions the final SQL must satisfy to be considered correct (e.g., 'Returns exactly 5 specific columns', 'Properly handles NULL values in the date column', 'Ensures no duplicate rows based on user_id').")
    estimated_complexity: Literal["simple","medium","complex"]

class CodeOutput(BaseModel):
    source_code: str = Field(description="The complete, executable source code generated to fulfill the request. Must include all necessary imports, adhere to language-specific formatting best practices, and contain inline comments explaining complex logic.")
    description: str = Field(description="A clear, high-level explanation of how the generated code works. Should detail the core algorithm, step-by-step execution instructions, required dependencies, and any key architectural decisions made.")

class ReviewOutput(BaseModel):
    verdict: Literal["APPROVED", "REVISION_NEEDED"] = Field(description="The final decision on the code's quality. Use 'APPROVED' if the code/SQL is fully correct, performant, and meets all specifications. Use 'REVISION_NEEDED' if bugs, vulnerabilities, or unhandled edge cases are found.")
    issues: list[str] = Field(description="A comprehensive list of discovered problems. This should include syntax errors, logical flaws, spec violations, performance bottlenecks (e.g., Cartesian products, inefficient joins), and unhandled edge cases (e.g., improper NULL handling or division by zero).")
    suggestions: list[str] = Field(description="Actionable, highly specific recommendations to fix the identified issues or optimize the code. Should include concrete SQL adjustments (e.g., 'Use LEFT JOIN instead of INNER JOIN', 'Replace subqueries with CTEs for readability'), or security fixes.")
    score: float = Field(ge=0.0,le=1.0,description="A quantitative evaluation of the code's overall quality, from 0.0 (completely broken or unsafe) to 1.0 (flawless, highly optimized, and production-ready). Considers correctness, efficiency, and readability.")