# Demonstrations: Using RAG-style Retrieval for Multiple Queries

## Executive summary

This report demonstrates three Retrieval-Augmented Generation (RAG) exercises using a combination of a local knowledge database and web sources. Each exercise shows the retrieval steps, the documents consulted, and a concise synthesized answer. The objective is to illustrate how RAG augments LLM outputs by grounding them in external documents and to highlight practical implementation and mitigation advice.

---

## Methodology

- Tools used: local knowledge database search, web search, and selective URL reading.
- Process per query: (1) query local database to check existing documentation, (2) web search to identify authoritative sources, (3) read 1-2 of the most relevant pages, (4) synthesize a grounded answer.
- Sources are listed in the Sources section. The report is focused and stops once sufficient facts were collected.

---

## Demonstration 1 — Query: "What is Retrieval-Augmented Generation (RAG)?"

Retrieval steps performed:
1. Local knowledge database search for "retrieval-augmented generation" (internal documents found describing RAG concept and overview).
2. Web search for the canonical academic reference and overview.
3. Read the NeurIPS/arXiv paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020) for formal definition and empirical findings.

Key points synthesized:
- Definition: RAG combines a parametric generative model (pretrained LLM) with a non-parametric retrieval component (an external document store) so the model can access up-to-date or domain-specific information at inference time.
- Architecture: typical components include a retriever (sparse or dense/vector), an index (e.g., FAISS, Annoy, Milvus), a reader/generator (seq2seq LLM), and optional reranker or fusion strategy.
- Benefits: improves factuality, allows dynamic knowledge updates, and provides a path to provenance (linking outputs to source documents).
- Variants: RAG formulations differ by how retrieved passages are conditioned during generation (e.g., conditioning on fixed set vs. per-token retrieval).

Representative citation used: Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020).

---

## Demonstration 2 — Query: "How to implement a RAG pipeline with FAISS and Hugging Face (practical steps)"

Retrieval steps performed:
1. Web search for practical tutorials and cookbooks (Hugging Face RAG cookbook, LangChain + FAISS tutorials).
2. Read the Hugging Face "Advanced RAG" cookbook (LangChain + Hugging Face tooling) to extract implementation recommendations.

Implementation summary (practical checklist):
- Prepare knowledge base: collect, clean, and chunk documents into semantically coherent snippets (use recursive chunking or sentence-aware splitters).
- Embed snippets: compute vector embeddings (e.g., SentenceTransformers, OpenAI embeddings) for each chunk.
- Index vectors: create a vector index using FAISS (or other vector DB) and persist it with metadata (source, doc id, start index).
- Retriever: at query time compute query embedding and perform k-NN search (top_k) against FAISS; optionally rerank results with cross-encoder or metadata filters.
- Reader/Generator: format prompt with retrieved snippets (respect token limits), include explicit instructions to the model to use only retrieved content and to respond conservatively if evidence is insufficient.
- Orchestration: use LangChain or direct Hugging Face inference pipelines to glue retrieval + generation, and include caching and fallback logic.
- Evaluation: test for accuracy, latency, and edge cases. Tune chunk size, top_k, and reranking.

Tuning notes from the cookbook:
- Chunk size and overlap are important: too large chunks dilute signal; too small chunks truncate meaning.
- Keep the total token footprint within the reader model limits to avoid "lost-in-the-middle" effects.
- Use metadata filtering (recency, source type) to bias retrieval towards reliable documents.

Representative references: Hugging Face Advanced RAG cookbook; community LangChain + FAISS examples.

---

## Demonstration 3 — Query: "What are best practices to reduce hallucinations in RAG systems?"

Retrieval steps performed:
1. Web search for mitigation strategies and enterprise guidance.
2. Read Microsoft's Azure AI Foundry blog on hallucination mitigation for LLMs, focusing on RAG-specific recommendations.

Best practices (synthesized):
- Data hygiene: curate and clean the knowledge base; ensure authoritative sources and remove duplicates/noisy documents.
- Retrieval quality: experiment with vector vs. hybrid search; apply reranking and metadata-based filters (e.g., recency, domain tags).
- Prompt engineering: instruct the generator explicitly to rely only on retrieved passages; include constraints like "If not supported by retrieved documents, respond 'Insufficient data.'"
- System defenses: implement system-level checks (content safety, RBAC, logging), and enforce provenance reporting (cite sources used for answers).
- Evaluation and feedback loops: use automated test suites, human-in-the-loop review for edge cases, and continuous monitoring for drift.
- Conservative decoding: lower temperature, use deterministic decoding (beam search), and ask the model to produce confidence judgments or to abstain when evidence is weak.

Microsoft guidance additionally emphasizes layered defenses: combine RAG grounding with prompt constraints, monitoring, and human review for high-risk applications.

---

## Short examples of prompt patterns (for grounding)

Example conservative prompt pattern to reduce hallucination:
- Instruction header: "Using ONLY the retrieved documents provided below, answer the user's question. If the documents do not contain enough information, reply 'Insufficient data.'"
- Retrieved evidence block: include top_k passages with source metadata.
- Question: include the user query and explicit output format constraints (e.g., 3 bullets + citations).

---

## Limitations and notes

- This report synthesizes authoritative sources, but a working RAG system requires iteration and domain-specific tuning.
- Implementation choices (index type, embedding model, reader LLM) are trade-offs among cost, latency, and accuracy.

---

## Sources

- Local knowledge database: retrieval-augmented-generation.pdf (internal)
- Lewis, P., Perez, E., Piktus, A., Karpukhin, V., Goyal, N., et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (NeurIPS/arXiv 2020). URL: https://arxiv.org/abs/2005.11401
- Hugging Face "Advanced RAG" cookbook (LangChain + Hugging Face). URL: https://huggingface.co/learn/cookbook/advanced_rag
- Microsoft Tech Community: "Best practices for mitigating hallucinations in large language models (LLMs)". URL: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/best-practices-for-mitigating-hallucinations-in-large-language-models-llms/4403129

---

(End of report)
