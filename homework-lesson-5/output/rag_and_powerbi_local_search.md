# Local Knowledge DB: Two Targeted Searches — RAG and Power BI

Objective

- Perform two targeted searches against the local knowledge database and summarize the top findings for each query. The queries were: "RAG" and "power bi".

Method

- Executed two local knowledge database searches and summarized the top 3 returned document excerpts for each.

Search 1 — Query: "RAG"

Top local results:
- retrieval-augmented-generation.pdf (Page 0) — Definition and high-level explanation of Retrieval-Augmented Generation (RAG): technique where LLMs retrieve and incorporate external documents into responses.
- retrieval-augmented-generation.pdf (Page 0 continued) — Notes on RAG reducing hallucinations and enabling use of domain-specific or up-to-date information (quote referencing Ars Technica).
- retrieval-augmented-generation.pdf (Page 1) — Overview/diagram of the RAG pipeline: combining external documents with user input to construct prompts for tailored LLM outputs.

Summary — RAG

- RAG allows LLMs to reference external documents (uploaded files, web sources, internal corpora) to produce answers grounded in source material.
- Benefits: up-to-date information access, domain specialization, and reduced hallucination risk through evidence-backed outputs.
- Typical pipeline elements: query encoding, similarity search (vector DB), document retrieval/selection, prompt construction (with retrieved context), and final LLM generation.

Search 2 — Query: "power bi"

Top local results:
- powerbi-intro.pdf (Page 6) — High-level introduction: Power BI connects to many data sources, supports visualization, publishing, and sharing of findings; can be used for personal reports up to enterprise-grade analytics.
- powerbi-intro.pdf (Page 6 continued) — Overview of Power BI components: Power BI Desktop, Power BI Service (SaaS), and Power BI mobile apps; these components form the backbone for creating, sharing, and consuming insights.
- powerbi-intro.pdf (Page 11) — Details about Power BI Service: where dashboards and reports are published and stored; mention of user access and publishing workflows.

Summary — Power BI

- Power BI is a versatile BI platform consisting of Desktop (authoring), Service (cloud publishing and sharing), and Mobile apps (consumption).
- It supports a broad range of data connectors and is suitable from ad-hoc desktop analytics to scalable enterprise-grade deployments.
- Typical usage involves building models/reports in Desktop, publishing to the Service, and sharing dashboards while managing access and data refresh.

Sources

- retrieval-augmented-generation.pdf (local knowledge base)
- powerbi-intro.pdf (local knowledge base)


