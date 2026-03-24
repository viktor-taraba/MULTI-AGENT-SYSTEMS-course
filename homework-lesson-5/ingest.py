from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config import data_dir, chunk_size, chunk_overlap, embedding_model, index_dir
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
load_dotenv()

"""
Knowledge ingestion pipeline.

Loads documents from data/ directory, splits into chunks,
generates embeddings, and saves the index to disk.

Usage: python ingest.py
"""

def load_documents():
    """ 1. Load documents from config.data_dir (PDF, TXT, MD) """

    if not os.path.exists(data_dir):
        print(f"Path not exist {data_dir}")
        return ""
    
    documents = []
    for root, dirs, files in os.walk(data_dir): # dirs - на випадок вкладених папок в data_dir
        for file in files:
            filepath = os.path.join(root, file)

            print(filepath)

            try:
                if file.lower().endswith(".pdf"):
                    loader = PyPDFLoader(filepath)
                    documents.extend(loader.load())
                elif file.lower().endswith((".txt", ".md")):
                    loader = TextLoader(filepath, encoding="utf-8")
                    documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {filepath}: {e}")

    for doc in documents:
        print(f"  Page: {doc.metadata['page']} | Length: {len(doc.page_content)} chars")

    return documents

    # ConfluenceLoader
    # YoutubeLoader
    # Docx2txtLoader - ms word
    # UnstructuredLoader - try for OCR for pdf

    # додати якусь обробку для битих пдф та чи треба для кирилиці?

    # метадані звідси теж зберігати

def documents_splitter(documents):
    """ 2. Split into chunks using TextSplitter """

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    recursive_chunks = recursive_splitter.split_documents(documents)
    print(f"Recursive splitter: {len(recursive_chunks)} chunks\n")

    for i, chunk in enumerate(recursive_chunks):
        print(f"Chunk {i} ({len(chunk.page_content)} chars)")
        print(chunk.page_content.strip())
        print("")

    return recursive_chunks

def ingest():
    # 1. Load documents from config.data_dir (PDF, TXT, MD)
    documents = load_documents()

    # 2. Split into chunks using TextSplitter
    chunks = documents_splitter(documents)
    
    # 3. Generate embeddings
    lc_embeddings = OpenAIEmbeddings(model=embedding_model)
    #print(lc_embeddings)

    """
    sample_chunks = [
    "Ось перший шматок тексту з нашого PDF.",
    "А це вже другий шматок тексту."
    ]

    vectors = lc_embeddings.embed_documents(sample_chunks)

    print("=== vectors ===")
    print(f"count vectors: {len(vectors)}")
    print(vectors)

    print(f"first vector: {vectors[0]}")
    print(f"second vector: {vectors[1]}")
    """

    # 4. Build vector store (FAISS, Qdrant, Chroma, etc.)
    # 5. Save index, chunks and metadata to config.index_dir
    os.makedirs(index_dir, exist_ok=True)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=lc_embeddings,
        persist_directory=index_dir,
        collection_name="test_collection"
    )

    # 6. Save chunks for BM25 retriever (pickle or JSON)
   
if __name__ == "__main__":
    ingest()