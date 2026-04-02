from langchain_core.documents import Document
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_classic.retrievers import ContextualCompressionRetriever
from config import (
    chunks_json_name, 
    chunks_dir, 
    embedding_model, 
    index_dir,
    retrieval_top_k,
    BM25_retriever_weight, 
    vector_retriever_weight,
    rerank_top_n,
    cross_encoder_model,
    collection_name
)
from dotenv import load_dotenv
import os
import json
import transformers
load_dotenv()

"""
Hybrid retrieval module.

Combines semantic search (vector DB) + BM25 (lexical) + cross-encoder reranking.
"""

# UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\Users\Viktor\.cache\huggingface\hub\models--BAAI--bge-reranker-base. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1" # disable Hugging Face progress bars e. g. Loading weights: 100%|██████████| 201/201 [00:00<00:00, 3189.31it/s]
transformers.logging.set_verbosity_error()
transformers.utils.logging.disable_progress_bar()

def load_bm25_chunks_from_json(chunks_path):
    """Load chunks"""
    if not os.path.exists(chunks_path):
        raise FileNotFoundError(f"Path {chunks_path} does not exist")
        
    with open(chunks_path, "r", encoding="utf-8") as f:
        loaded_dicts = json.load(f)
        
    chunks = [
        Document(page_content=item["page_content"], metadata=item["metadata"]) 
        for item in loaded_dicts
    ]
    return chunks

def format_docs_for_llm(results):
    """Formatting output"""
    formatted_texts = []
    for i, doc in enumerate(results):
        source = doc.metadata.get('source', 'Unknown').split('\\')[-1]
        page = doc.metadata.get('page', 'Unknown')
        
        doc_string = f"--- Document {i+1} ---\n"
        doc_string += f"Source: {source} (Page: {page})\n"
        doc_string += f"Content:\n{doc.page_content.strip()}\n"
        
        formatted_texts.append(doc_string)
        
    return "\n".join(formatted_texts)

_cached_retriever = None

def get_retriever(query_text: str):
    """Main retriever function"""
    # 1. Load vector store from disk (config.index_dir)
    global _cached_retriever

    if _cached_retriever is None:
        
        lc_embeddings = OpenAIEmbeddings(model=embedding_model)

        vectorstore = Chroma(
            persist_directory=index_dir,
            embedding_function=lc_embeddings,
            collection_name=collection_name
        )

        # 2. Create semantic retriever from vector store
        vector_retriever = vectorstore.as_retriever(search_kwargs={"k": retrieval_top_k})

        # 3. Load chunks and create BM25 retriever
        chunks = load_bm25_chunks_from_json(os.path.join(chunks_dir,chunks_json_name))
        bm25_retriever = BM25Retriever.from_documents(chunks)
        bm25_retriever.k = retrieval_top_k

        # 4. Combine into ensemble retriever (semantic + BM25)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            weights=[BM25_retriever_weight, vector_retriever_weight]
        )

        # 5. Add cross-encoder reranker on top
        reranker_model = HuggingFaceCrossEncoder(model_name=cross_encoder_model)
        compressor = CrossEncoderReranker(
            model=reranker_model,
            top_n=rerank_top_n
        )

        _cached_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=ensemble_retriever
        )

    # 6. Return the final retriever
    results = _cached_retriever.invoke(query_text)
    return format_docs_for_llm(results)