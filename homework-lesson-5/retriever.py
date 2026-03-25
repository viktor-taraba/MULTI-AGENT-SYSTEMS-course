from langchain_core.documents import Document
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import (
    chunks_json_name, 
    chunks_dir, 
    embedding_model, 
    index_dir
)
from dotenv import load_dotenv
import os
import json
load_dotenv()
# pip install rank_bm25

"""
Hybrid retrieval module.

Combines semantic search (vector DB) + BM25 (lexical) + cross-encoder reranking.
"""

def load_bm25_chunks_from_json(chunks_path):
    """Load chunks and create BM25 retriever"""
    if not os.path.exists(chunks_path):
        raise FileNotFoundError(f"Path {chunks_path} does not exist")
        
    with open(chunks_path, "r", encoding="utf-8") as f:
        loaded_dicts = json.load(f)
        
    chunks = [
        Document(page_content=item["page_content"], metadata=item["metadata"]) 
        for item in loaded_dicts
    ]
    return chunks

def get_retriever():
    # TODO:

    # 1. Load vector store from disk (config.index_dir)
    lc_embeddings = OpenAIEmbeddings(model=embedding_model)

    vectorstore = Chroma(
        persist_directory=index_dir,
        embedding_function=lc_embeddings,
        collection_name="documents_collection"
    )

    # 2. Create semantic retriever from vector store
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # 3. Load chunks and create BM25 retriever
    chunks = load_bm25_chunks_from_json(chunks_dir+"/"+chunks_json_name)
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 10

    query = "Power development"
    print(f"BM25 search: '{query}'\n")

    results = bm25_retriever.invoke(query)
    for i, doc in enumerate(results[:10]):
        print(f"Result {i+1}:")
        print(f"  Source: {doc.metadata.get('source', 'unknown')}")
        print(f"  Content: {doc.page_content[:150]}...")
        print()

    print("---------------------------------------------------")
    print(f"\nSemantic search: '{query}'\n")

    results_vector = vector_retriever.invoke(query)
    for i, doc in enumerate(results_vector[:10]):
        print(f"Result {i+1}:")
        print(f"  Source: {doc.metadata.get('source', 'unknown')}")
        print(f"  Content: {doc.page_content[:150]}...")
        print()

    # 4. Combine into ensemble retriever (semantic + BM25)
    ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # 40% BM25 + 60% Vector
    )

    print("---------------------------------------------------")
    print(f"\nEnsemble search: '{query}'\n")

    results = ensemble_retriever.invoke(query)
    for i, doc in enumerate(results[:10]):
        print(f"Result {i+1}:")
        print(f"  Source: {doc.metadata.get('source', 'unknown')}")
        print(f"  Content: {doc.page_content[:150]}...")
        print()

    # 5. Add cross-encoder reranker on top

    # 6. Return the final retriever

    pass

get_retriever()