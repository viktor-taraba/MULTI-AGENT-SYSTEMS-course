# LLM and DAX — Summary Report

## Executive summary
- This concise report summarizes local knowledge-base findings on Large Language Models (LLMs) and Data Analysis Expressions (DAX). It outlines definitions, core properties, operational considerations, and practical intersections where LLMs can assist Power BI/DAX workflows.

## Methodology
- Performed two focused searches of the local knowledge database (RAG): one for "LLM" and one for "DAX". Key internal documents were reviewed and synthesized. Sources are listed at the end of the document.

---

## 1. Large Language Models (LLMs)

Definition and scope
- LLMs are foundation models trained on large corpora of text to predict or generate sequences. They consist of billions to trillions of parameters and generalize across tasks with minimal task-specific supervision.

Training and costs
- Typical training involves pretraining on next-token prediction and optional fine-tuning. Training large models requires substantial infrastructure: an example cited is GPT-2 (1.5B parameters) with nontrivial costs.

Capabilities and limitations
- Capabilities: generation, summarization, translation, reasoning, and cross-task generalization.
- Limitations: inherit biases and inaccuracies from training data; are prone to hallucinations if asked about out-of-distribution facts.

Prompting techniques
- Chain-of-thought / step-by-step prompting: giving examples where the model shows intermediate reasoning steps improves correctness on complex tasks (e.g., math problems).

Implications for BI and analytics
- LLMs can be used as copilots to explain logic, generate or correct DAX expressions, create documentation, and help craft natural-language queries for semantic layers. However, outputs should be validated because of potential inaccuracies.


## 2. Data Analysis Expressions (DAX)

Overview
- DAX is the formula language used in Power BI Desktop, Power Pivot, and Analysis Services. It is optimized for BI analytics and differs from SQL in evaluation context and function set.

Key concepts
- Evaluation contexts: row context and filter context are central. Functions like CALCULATE modify filter context and are foundational to complex measures.
- Use measures (calculated at query time) instead of calculated columns when possible for performance.

Representative functions and constructs
- AVERAGEX: an iterator that evaluates an expression across rows of a table and returns the arithmetic mean of the results. Applies to calculated columns, calculated tables, and measures.
- Time intelligence: DAX supports calendar-based time-intelligence functions and relies on a properly modeled date/calendar table. Newer guidance and features refine how dependencies and REMOVEFILTERS operate for time calculations.
- Dependency handling: DAX identifies column category dependencies (e.g., Year, Month of Year) to decide which filters to remove or apply when functions like REMOVEFILTERS are used.

Practical notes
- DAX differs from SQL: it is expression-based and context-driven; learners coming from SQL should focus on filter and row contexts.
- Documentation and structured examples (such as function pages like AVERAGEX) are valuable for learning correct usage and visual calculation behavior.


## 3. Cross-Topics — LLMs supporting DAX and Power BI

- Code generation: LLMs can draft DAX measures or suggest optimizations, but outputs must be validated against the model and dataset because of potential semantic errors.
- Explainability: LLMs can translate DAX into plain-language explanations of what a measure does, useful for documentation and onboarding.
- Prompting strategy: Use step-wise prompting (chain-of-thought) and provide context (data model description, sample tables) to improve quality of generated DAX.
- RAG approach: Combining an LLM with a retrieval layer that supplies authoritative DAX documentation, model definitions, or internal style guides reduces hallucination risk and improves accuracy when generating or explaining DAX.


## 4. Recommendations

For teams adopting LLM-assisted DAX workflows
1. Provide context: always supply the model with data model schema, sample rows, and coding conventions.
2. Validate outputs: implement automated unit tests where feasible (sample data rows expected outputs) and peer review for generated DAX.
3. Use RAG: integrate retrieval of authoritative DAX documentation and internal examples to condition LLM responses.
4. Train users on limitations: make consumers aware that LLMs can hallucinate and require verification.

For analysts learning DAX
- Focus first on understanding evaluation contexts (row vs filter) and CALCULATE. Then practice iterator functions (SUMX, AVERAGEX) and time-intelligence scenarios using a calendar table.


---

## Sources
- large-language-model.pdf (pages: 0, 4, 8) — local knowledge database
- Tips and tricks for creating reports in Power BI Desktop.docx — local knowledge database
- DAX AVERAGEX.pdf (page: 0) — local knowledge database
- introducing-calendar-based-time-intelligence-in-dax.pdf (page: 5) — local knowledge database


