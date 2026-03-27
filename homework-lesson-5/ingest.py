from langchain_community.document_loaders import PyPDFLoader, TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config import (
    data_dir, 
    chunk_size, 
    chunk_overlap, 
    embedding_model, 
    index_dir, 
    chunks_dir, 
    chunks_json_name
)
from langchain_chroma import Chroma
from langchain_community.document_loaders import YoutubeLoader 
# pip install youtube-transcript-api
import os
from dotenv import load_dotenv
import chromadb
import hashlib
import json
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
    for root, dirs, files in os.walk(data_dir): # dirs - if there are additional folder in data_dir
        for file in files:
            filepath = os.path.join(root, file)
            file_docs = []

            try:
                if file.lower().endswith(".pdf"):
                    loader = PyPDFLoader(filepath)
                    file_docs = loader.load()

                    total_text_length = sum(len(doc.page_content.strip()) for doc in file_docs)

                    # try with PyMuPDFLoader if no text found with PyPDFLoader
                    if total_text_length == 0:
                        fallback_loader = PyMuPDFLoader(filepath)
                        file_docs = fallback_loader.load()
                        
                elif file.lower().endswith((".txt", ".md")):
                    loader = TextLoader(filepath, encoding="utf-8")
                    file_docs = loader.load()

                # other formets
                else:
                    continue

                # exclude empty pages
                for doc in file_docs:
                    if doc.page_content.strip(): 
                        documents.append(doc)
               
            except Exception as e:
                print(f"Error loading {filepath}: {e}")

    if documents:
        print(f"STEP 1. Load documents from config.data_dir (PDF, TXT, MD) - FINISHED ({len(documents)} pages)\n")

    return documents

def documents_splitter(documents):
    """ 2. Split into chunks using TextSplitter """

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    recursive_chunks = recursive_splitter.split_documents(documents)

    if recursive_chunks:
        print(f"STEP 2. Split into chunks using TextSplitter - FINISHED ({len(recursive_chunks)} chunks)\n")

    return recursive_chunks

def save_chunks_for_BM25(chunks):
    """ # 6. Save chunks for BM25 retriever """
    os.makedirs(chunks_dir, exist_ok=True)
    bm25_file_path = os.path.join(chunks_dir, chunks_json_name)
    
    chunks_dict = [
        {
            "page_content": chunk.page_content,
            "metadata": chunk.metadata
        } 
        for chunk in chunks
    ]

    with open(bm25_file_path, "w", encoding="utf-8") as f:
        json.dump(chunks_dict, f, ensure_ascii=False, indent=4)

    print(f"STEP 6. Save chunks for BM25 retriever (json) - FINISHED ({len(chunks)} chunks)\n")

def ingest():
    # 1. Load documents from config.data_dir (PDF, TXT, MD)
    documents = load_documents()

    # 2. Split into chunks using TextSplitter
    chunks = documents_splitter(documents)
    
    # це винести в окрему функцію
    # 3. Generate embeddings
    # 4. Build vector store (Qdrant)
    # 5. Save index, chunks and metadata to config.index_dir
    lc_embeddings = OpenAIEmbeddings(model=embedding_model)

    os.makedirs(index_dir, exist_ok=True)
    vectorstore = Chroma(
        persist_directory=index_dir,
        embedding_function=lc_embeddings,
        collection_name="documents_collection"
    )

    # solving duplicates problems with hash ids
    existing_items = vectorstore.get()
    existing_ids = set(existing_items["ids"])
    new_chunks, new_ids  = [], []
    current_ids = set()

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown_source")
        unique_string = f"{source}::{chunk.page_content}"

        chunk_hash = hashlib.sha256(unique_string.encode("utf-8")).hexdigest()
        current_ids.add(chunk_hash)

        if chunk_hash not in existing_ids:
            new_chunks.append(chunk)
            new_ids.append(chunk_hash)

    ids_to_delete = existing_ids - current_ids
    if ids_to_delete:
        vectorstore.delete(ids=list(ids_to_delete))
    
    if new_chunks:
        vectorstore.add_documents(documents=new_chunks, ids=new_ids)
    else:
        print("All documents are already in the index, no need to repeat embedding\n")

    print("STEP 3. Generate embeddings - FINISHED\n")
    print("STEP 4. Build vector store (Chroma) - FINISHED\n")
    print(f"STEP 5. Save index, chunks and metadata to {index_dir}) - FINISHED ({len(new_chunks)} new chunks added, {len(ids_to_delete)} deleted)\n")

    # 6. Save chunks for BM25 retriever (json)
    save_chunks_for_BM25(chunks)

if __name__ == "__main__":
    ingest()


def YoutubeText_loader(video_url):
    """load text (subtitles) from YouTube videos"""
    loader = YoutubeLoader.from_youtube_url(
        video_url, 
        add_video_info=False # Ставимо False, якщо нам потрібен ТІЛЬКИ текст (працює швидше)
    )
    docs = loader.load()

    print(f"Завантажено документів: {len(docs)}")
    print("\n--- Фрагмент тексту відео ---")
    print(docs[0].page_content[:500])

    # YoutubeText_loader("https://www.youtube.com/watch?v=53blGRa45V0")

    # ConfluenceLoader
    # YoutubeLoader
    # Docx2txtLoader - ms word
    # позагортати в try except