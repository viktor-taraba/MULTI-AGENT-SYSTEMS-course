# What is RAG (Retrieval-Augmented Generation)

## Executive summary

Retrieval-Augmented Generation (RAG) is a hybrid approach that combines parametric language models (e.g., BART, T5, GPT-style models) with an external, non-parametric retrieval component (an indexed document store). At inference time, the model retrieves relevant documents or passages and conditions its generation on those retrieved texts. RAG improves factual accuracy, enables provenance, supports knowledge updates without full model retraining, and is widely used for open-domain question answering, knowledge-grounded dialogue, and other knowledge-intensive NLP tasks.

## Core idea

Instead of relying solely on knowledge stored in model weights, RAG supplements a generative model with retrieved textual evidence. The generator conditions on retrieved passages (and optionally on different passages per token) to produce answers grounded in external sources.

## Main components

- Retriever: finds relevant documents/passages for a given query. Can be sparse (BM25) or dense (bi-encoders such as DPR). Dense retrievers use vector similarity (FAISS, Milvus, etc.).
- Document index / store: the non-parametric memory (e.g., Wikipedia dump tokenized into passages and embedded) stored in a specialized index.
- Generator (parametric model): a seq2seq or decoder-only LM (BART, T5, GPT) that conditions on retrieved passages plus the query to generate text.
- (Optional) Reranker or scorer: reorders or filters retrieved candidates before generation.

## Two standard RAG formulations (from Lewis et al.)

- RAG-Sequence (RAG-Seq): retrieves a fixed set of passages and conditions the generator on the concatenation of each passage paired with the query; the generator marginalizes across passages by scoring each passage-conditioned output sequence and summing probabilities.
- RAG-Token: allows the generator to attend to different passages for each generated token, effectively mixing evidence token-wise. This formulation is more flexible but computationally heavier.

## How a typical RAG inference works (step-by-step)

1. Receive query or prompt.
2. Retrieve top-k candidate passages from the index using the retriever.
3. Optionally rerank or deduplicate passages.
4. Feed the query plus retrieved passages into the generator (either concatenated or via per-token conditioning depending on RAG variant).
5. Decode an output (greedy/beam/sampling) that is grounded in retrieved text.
6. Optionally return provenance: links/IDs of the retrieved passages used.

## Benefits

- Reduced hallucinations: grounding generation in retrieved facts reduces unsupported assertions.
- Updatable knowledge: updating the index is cheaper than re-training a large model.
- Explainability/provenance: systems can return the source passages that supported an answer.
- Improved performance on knowledge-intensive tasks: demonstrated SOTA on several open-domain QA benchmarks in the original RAG paper.

## Limitations and risks

- Retrieval quality is critical: bad or missing documents produce poor outputs.
- Latency and cost: retrieval + generation adds runtime and infrastructure complexity compared to a single LLM call.
- Hallucinations still possible: the generator can misinterpret or overgeneralize from retrieved passages.
- Index maintenance: building and keeping the index up-to-date and consistent requires engineering.
- Token-length and context window limits: concatenating many passages can hit encoder context limits.

## Implementation choices and tooling

- Retriever options: BM25 (Lucene/ElasticSearch), dense retrievers (DPR, SBERT), or newer methods (colBERT, SPLADE).
- Indexing & vector stores: FAISS (CPU/GPU), Milvus, Qdrant, Weaviate, Pinecone.
- Generators: BART, T5, Flan-T5, or decoder-only models adapted for conditioning on text. Hugging Face Transformers includes RAG utilities and example implementations.
- Rerankers: cross-encoders or re-ranking neural models to improve passage ordering.

## Evaluation metrics

- For QA: Exact Match (EM), F1.
- For generative tasks: ROUGE / BLEU / BERTScore and human evaluation of factuality and fluency.
- Retrieval metrics: recall@k, MRR (for the retriever itself).

## Common use cases

- Open-domain question answering (Wikipedia or curated corpora).
- Knowledge-grounded chatbots and assistants.
- Domain-specific document retrieval + summarization (legal, medical, enterprise knowledge bases).
- Long-context generation aided by chunked knowledge retrieval.

## Practical considerations

- Passage chunking: documents are typically split into passage-sized chunks (e.g., 100–300 tokens) before embedding.
- Hybrid retrieval: combining BM25 and dense retrieval often improves coverage.
- Cache and latency optimizations: caching recent retrievals, approximate nearest neighbor (ANN) indexes for speed.
- Provenance handling: include passage IDs and snippet offsets to support traceability and audits.

## Variants and research directions

- Generative rerankers and reinforced retrieval: learning to retrieve passages that maximize downstream generation quality.
- Parametric-RAG hybrids: combining closed-book parametric knowledge and open-book retrieval more tightly.
- Retrieval for instruction following and in-context retrieval to improve long-form generation.

## Short technical glossary

- Non-parametric memory: data stored outside the model weights (e.g., document index).
- Dense retriever: embedding-based retriever using vector similarity.
- FAISS: Facebook AI Similarity Search library for ANN and vector indexing.
- DPR: Dense Passage Retrieval (bi-encoder retriever trained for QA retrieval).

## Further reading (key references)

- Lewis, P., Perez, E., Piktus, A., Karpukhin, V., Goyal, N., Küttler, H., ... & Riedel, S. (2021). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. arXiv:2005.11401. https://arxiv.org/abs/2005.11401
- Hugging Face paper summary and resources for RAG: https://huggingface.co/papers/2005.11401

## Sources

- https://arxiv.org/abs/2005.11401
- https://huggingface.co/papers/2005.11401
