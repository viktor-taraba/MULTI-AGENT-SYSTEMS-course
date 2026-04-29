# LLM and DAX — Local Knowledge Summary (Repeat)

## Executive Summary
This document summarizes findings from two focused searches of the local knowledge database: one for "LLM" (Large Language Models) and one for "DAX" (Data Analysis Expressions). The report highlights definitions, core properties, common limitations, and practical recommendations for combining LLMs with DAX/Power BI workflows.

## Method
- Performed two RAG-style local database searches (LLM and DAX).
- Synthesized content from the most relevant internal documents and produced concise guidance and recommendations.


## 1. Large Language Models (LLMs)

Definition
- LLMs are foundation models trained on large text corpora to model language. They can range from billions to trillions of parameters and generalize across tasks with minimal task-specific supervision.

Training approach and costs
- Typical process: unsupervised pretraining (next-token prediction) followed by optional fine-tuning. Training large models requires substantial compute and infrastructure; even earlier large models like GPT-2 (1.5B parameters) incurred significant costs.

Strengths
- Strong capabilities in text generation, summarization, translation, and certain forms of reasoning.
- Effective at generalizing across a variety of NLP tasks with few-shot or zero-shot prompting.

Limitations
- Inherit biases and inaccuracies from training data.
- Susceptible to hallucinations — may produce plausible-sounding but incorrect statements.

Useful prompting patterns
- Chain-of-thought or stepwise prompting: encouraging the model to produce intermediate reasoning steps improves accuracy on complex tasks.

Business implications
- LLMs are valuable as copilots: generating explanations, code (including DAX), documentation, and natural-language queries for semantic layers. Outputs must be validated before production use.


## 2. Data Analysis Expressions (DAX)

Overview
- DAX is the formula language for Power BI, Power Pivot, and Analysis Services. It is optimized for BI scenarios and uses evaluation contexts that differ from SQL.

Core concepts
- Evaluation contexts: row vs filter context; CALCULATE is fundamental for modifying filter context and enabling advanced calculations.
- Prefer measures (calculated at query time) to calculated columns where possible to improve model performance.

Notable functions and features
- Iterator functions (e.g., AVERAGEX) evaluate expressions row-by-row over a table and are essential for complex aggregations.
- Time intelligence: relies on a well-constructed date/calendar table and dependency handling when using functions like REMOVEFILTERS across date hierarchies.

Learning advice
- Focus on understanding filter propagation, CALCULATE, and iterator vs aggregator functions. Use official documentation and examples to practice common patterns.


## 3. Integrating LLMs and DAX — Practical Guidance

- Use LLMs to draft or explain DAX measures, but always validate generated expressions in the model context.
- Provide the LLM with schema, sample data, and coding conventions to reduce errors.
- Combine LLMs with a retrieval layer (RAG) that supplies authoritative DAX documentation and internal examples to improve accuracy.
- Where possible, implement automated tests or sample-case validations for generated measures.


## 4. Recommendations
- For teams: Establish a validation workflow for any LLM-generated DAX, including peer review and unit tests on sample data.
- For analysts learning DAX: Invest time in evaluation context concepts and practice with iterator functions and time intelligence scenarios.


---

## Sources
- large-language-model.pdf (local knowledge database)
- Tips and tricks for creating reports in Power BI Desktop.docx (local knowledge database)
- DAX AVERAGEX.pdf (local knowledge database)
- introducing-calendar-based-time-intelligence-in-dax.pdf (local knowledge database)

