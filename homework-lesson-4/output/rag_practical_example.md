# Practical example: Realizing a RAG system

## Executive summary

This document provides a concrete, step-by-step practical realization of a Retrieval-Augmented Generation (RAG) system. Two example implementations are given: (A) LangChain + Pinecone + OpenAI (cloud-managed vector DB + hosted LLM) and (B) Hugging Face Transformers + FAISS + DPR (fully open-source stack). Each example includes architecture, code snippets, configuration choices, deployment considerations, and practical tips for production.

---

## System architecture (common patterns)

Core components:
- Ingestion and chunking: split documents into passage-sized chunks (100–1000 tokens) and attach metadata (source, doc id, offsets).
- Embedding encoder (retriever): encodes passages and queries into vectors (SentenceTransformers, OpenAI embeddings, or Pinecone Inference embeddings).
- Vector index / store: FAISS / Milvus / Qdrant / Pinecone / Weaviate to store embeddings and provide ANN search.
- Reranker (optional): cross-encoder to reorder top-k retrieved passages.
- Generator (reader): seq2seq or decoder-only LLM that conditions on retrieved passages to generate answers (e.g., Flan-T5, BART, GPT-3.5/4).
- Orchestration: glue code that performs retrieve -> (rerank) -> generate and returns provenance.

Typical inference flow:
1. Query received.
2. Retriever returns top-k passages (IDs + text + score).
3. (Optional) Reranker reorders top-n.
4. Generator receives the query + concatenated passages (or uses RAG token/seq formulation) and decodes an answer.
5. System returns answer plus provenance (passage IDs/URLs and scores).

---

## Example A: LangChain + Pinecone + OpenAI (cloud-friendly)

When to choose: easiest to implement, minimal infra to manage, good for production quickly when using hosted OpenAI + Pinecone.

High-level steps:
1. Install libraries

```bash
pip install langchain pinecone-client openai tiktoken python-dotenv
```

2. Environment variables (Pinecone & OpenAI keys)

```bash
export PINECONE_API_KEY="<PINECONE_KEY>"
export PINECONE_ENV="<PINECONE_ENV>" # e.g., us-west1-gcp
export OPENAI_API_KEY="<OPENAI_KEY>"
```

3. Ingest and chunk documents using LangChain text splitters

- Use RecursiveCharacterTextSplitter or SentenceSplitter. Choose chunk_size ~ 500 tokens, overlap ~ 5000 tokens depending on document structure.

4. Create embeddings and upsert into Pinecone

```python
from langchain.embeddings import OpenAIEmbeddings
import pinecone

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index_name = "my-rag-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)
index = pinecone.Index(index_name)

emb = OpenAIEmbeddings()
# articles -> chunks list of (id, text, metadata)
vectors = [(chunk_id, emb.embed_query(text), metadata) for chunk_id, text, metadata in chunks]
index.upsert(vectors)
```

5. Query-time retrieval + generation with LangChain

```python
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

vectorstore = Pinecone(index, embedding=emb)
llm = ChatOpenAI(model_name="gpt-4o-mini") # or gpt-3.5-turbo
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(search_kwargs={"k": 4}))

# ask
result = qa.run("What are the warranty terms for the WonderVector5000?")
print(result)
```

6. Provenance: return `retriever.get_relevant_documents(query)` results with metadata (source, offsets) and confidence scores.

Operational tips for this stack:
- Use Pinecone namespaces for multi-tenant data separation.
- Use hybrid retrieval (BM25 + dense) if documents are noisy.
- Monitor usage/cost: OpenAI + Pinecone can be expensive; add query-rate limits and caching.

---

## Example B: Hugging Face Transformers + FAISS + DPR (open-source)

When to choose: full control, lower recurring costs, runs on your infra or cloud VMs; better for privacy-sensitive data.

High-level steps:
1. Install packages

```bash
pip install transformers datasets faiss-cpu sentence-transformers accelerate
```

2. Ingest & chunk documents into passages with metadata.

3. Build passage embeddings with DPR or SentenceTransformers

```python
from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer('all-mpnet-base-v2')
embs = embedder.encode([p['text'] for p in passages], show_progress_bar=True)
```

4. Create FAISS index and persist

```python
import faiss
d = embs.shape[1]
index = faiss.IndexFlatIP(d)  # inner product (with normalized vectors for cosine)
faiss.normalize_L2(embs)
index.add(embs)
faiss.write_index(index, 'passages.index')
# store metadata map (id -> metadata) separately (e.g., JSON or DB)
```

5. Retrieve top-k and pass to generator (Hugging Face RAG or seq2seq LLM)

Option 1: Use Hugging Face RAG model (RagTokenizer + RagRetriever + RagSequenceForGeneration)

```python
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq", index_name="custom", passages_path="my_passages.json")
model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq", retriever=retriever)

input_text = "Who developed the WonderVector5000?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.batch_decode(outputs, skip_special_tokens=True))
```

Note: Hugging Face's built-in retriever expects specific passage stores. You can adapt the architecture by implementing a custom Retriever that queries FAISS and returns passages.

Option 2: Use a standard seq2seq LLM (Flan-T5) and concatenate top-k passages into the prompt/context

```python
# retrieve topk ids and texts from FAISS
# build prompt: [CONTEXT]\nPassage1... PassageK\nQuestion: ...
# call Flan-T5 or other model
```

Operational tips for this stack:
- Persist FAISS index on fast SSDs; use GPU FAISS (faiss-gpu) for lower latency at scale.
- Serialize metadata in a key-value store (Redis / simple DB) to look up passage text and provenance.
- Reranking with a cross-encoder (e.g., cross-encoder/ms-marco-MiniLM-L-6-v2) often improves final answer quality.

---

## Key implementation details & tuning

- Chunk size and overlap: 200000 tokens chunking (typical 30000 tokens) with 105% overlap balances context and retrieval recall.
- Embedding model: choose dimensionality/performance tradeoff: `all-mpnet-base-v2` (768 dim) or OpenAI embeddings (1536 dim).
- top_k (retrieval): start with 3 and tune; higher k raises chance of including relevant passages but increases noise.
- Reranker: use a cross-encoder to rerank top-50 down to top-5 for generation.
- Caching: cache recent queries and retrieval results to save costs and reduce latency.
- Prompt engineering: include retrieved passages as explicit evidence and ask the generator to cite sources (e.g., "Answer using only the passages below; cite source IDs").

---

## Evaluation and monitoring

- Retrieval metrics: recall@k, MRR on a held-out QA set.
- Generation metrics: Exact Match (EM) / F1 for QA, BERTScore / human eval for generative quality.
- Production telemetry: latency (retrieval + generation), p95/p99, cost per query, token usage, error rates.
- Safety checks: monitor hallucinations by sampling outputs and verifying against provenance.

---

## Deployment & scaling considerations

- Low-latency: run retriever on SSDs or vector DB with GPU/CPU ANN tuned; use batch embedding/lookup for throughput.
- Multi-tenant: use namespaces in vector DB (Pinecone) or separate indices with per-tenant quotas.
- Security & privacy: encrypt data at rest, control access to vector DBs and embedding APIs; consider on-premise embedding + index for sensitive data.
- Updates: support incremental upserts and deletions to the vector index; schedule re-embedding if embedding model changes.

---

## Common pitfalls

- Feeding too many passages and hitting model context window (Lost-in-the-middle). Keep total tokens reasonable.
- Relying on a single retrieval model: use hybrid retrieval and reranking for robustness.
- Not storing provenance: without it, it's difficult to debug hallucinations or comply with audits.

---

## Example cost & latency tradeoffs (rules of thumb)

- Hosted LLM (OpenAI) + Pinecone: low infra ops but higher per-query cost and vendor dependence.
- Self-hosted LLM + FAISS: higher infra ops and latency tuning needed, lower per-query API expense.
- FAISS GPU can reduce retrieval latency for large corpora but requires GPU infra.

---

## Short checklist to go from POC to Production

1. Clear data ingestion pipeline with metadata and chunking.
2. Stable embedding and index pipeline with backups and versioning.
3. Reranker and prompt template to reduce hallucinations.
4. Provenance collection and logging.
5. Metrics and alerting for latency, quality, and cost.
6. Security and tenant isolation.

---

## Sources

- Lewis, P. et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (arXiv): https://arxiv.org/abs/2005.11401
- Hugging Face: Advanced RAG cookbook (LangChain integration): https://huggingface.co/learn/cookbook/advanced_rag
- Pinecone: Build a RAG chatbot tutorial: https://docs.pinecone.io/guides/get-started/build-a-rag-chatbot

