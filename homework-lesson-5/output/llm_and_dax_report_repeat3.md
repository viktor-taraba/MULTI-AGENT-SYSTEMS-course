# LLM and DAX — Local Knowledge Brief (Iteration 3)

## Executive summary
This brief consolidates findings from local knowledge-base searches on Large Language Models (LLMs) and Data Analysis Expressions (DAX). It restates definitions, core strengths and limitations, practical guidance for combining LLMs with DAX workflows, and recommendations to ensure safe and effective use.

## Methodology
- Two targeted local searches were executed: one for "LLM" and one for "DAX".
- Extracted and synthesized key points from internal documents covering model behavior, DAX language constructs, and practical usage tips.


## 1. Large Language Models (LLMs)

What they are
- LLMs are foundation models trained on large corpora to model and generate language. They typically contain billions or more parameters and perform many NLP tasks with minimal task-specific tuning.

Training pattern and resource implications
- Standard approach: pretrain on next-token prediction followed by optional fine-tuning. Training large models requires substantial compute; historical examples (e.g., GPT-2) demonstrate non-trivial costs even for earlier large models.

Capabilities
- Text generation, summarization, translation, reasoning, and few-shot generalization across diverse tasks.

Limitations and risks
- Bias and inaccuracies inherited from training data.
- Hallucinations: produce plausible but incorrect outputs.

Prompting improvements
- Chain-of-thought or stepwise prompting improves correctness for complex reasoning tasks by eliciting intermediate steps.


## 2. Data Analysis Expressions (DAX)

Overview
- DAX is the formula language for Power BI, Power Pivot, and Analysis Services, optimized for BI analytics and calculation expressions.

Core concepts
- Evaluation contexts: row context vs filter context; mastery of CALCULATE is essential.
- Prefer measures over calculated columns for dynamic and performant calculations.

Representative functions
- Iterator functions (e.g., AVERAGEX) evaluate expressions row-by-row across tables.
- Time-intelligence functions depend on a properly modeled calendar table and careful handling of filter removal (e.g., REMOVEFILTERS behavior across date hierarchies).

Practical learning advice
- Emphasize understanding filter propagation, CALCULATE usage, and iterator semantics through worked examples.


## 3. Practical integration: LLMs assisting DAX workflows

- Use LLMs to draft or explain DAX, but require validation: LLM outputs can speed up development and documentation but must be checked for correctness.
- Provide contextual inputs (data model schema, column names, sample rows) to reduce errors in generated DAX.
- Use RAG to supply authoritative DAX references and internal style guides to the LLM for more reliable outputs.
- Automate validation where possible: create test cases or known-sample outputs to verify generated measures behave as expected.


## 4. Recommendations
- Implement a validation pipeline for LLM-generated DAX (peer review + unit/sample tests).
- Maintain a retrieval index of official DAX documentation and internal examples for use with RAG-enabled assistants.
- Train analysts on DAX fundamentals (evaluation contexts, CALCULATE, iterators) before relying on LLM assistance.


---

## Sources
- large-language-model.pdf (local knowledge database)
- Tips and tricks for creating reports in Power BI Desktop.docx (local knowledge database)
- DAX AVERAGEX.pdf (local knowledge database)
- introducing-calendar-based-time-intelligence-in-dax.pdf (local knowledge database)

