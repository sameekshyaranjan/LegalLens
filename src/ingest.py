"""
ingest.py — Document Ingestion Pipeline

Handles the full ingestion flow:
  1. Load PDF documents from /data
  2. Split into semantic chunks
  3. Generate embeddings via Google Gemini
  4. Persist FAISS vector store to /vectordb
"""

import os
import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATA_DIR,
    EMBEDDING_MODEL,
    GEMINI_API_KEY,
    VECTORDB_DIR,
)
from src.utils import print_error, print_separator, print_status, print_success


def load_pdfs(data_dir: Path = DATA_DIR) -> list:
    """Load all PDF documents from the data directory.

    Each page is loaded as a separate Document with metadata containing
    the source filename and page number.

    Args:
        data_dir: Path to the directory containing PDF files.

    Returns:
        List of LangChain Document objects.

    Raises:
        SystemExit: If no PDF files are found.
    """
    pdf_files = list(data_dir.glob("*.pdf"))

    if not pdf_files:
        print_error(f"No PDF files found in {data_dir}")
        print("  Please add PDF files to the 'data/' directory and try again.")
        sys.exit(1)

    all_documents = []

    for pdf_path in pdf_files:
        print_status(f"Loading: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()

        # Enrich metadata with clean source filename
        for doc in documents:
            doc.metadata["source"] = pdf_path.name

        all_documents.extend(documents)

    print_success(f"Loaded {len(all_documents)} pages from {len(pdf_files)} PDF(s)")
    return all_documents


def split_documents(
    documents: list,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list:
    """Split documents into smaller chunks for embedding.

    Uses RecursiveCharacterTextSplitter to preserve semantic continuity
    across chunk boundaries.

    Args:
        documents: List of LangChain Document objects.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of overlapping characters between chunks.

    Returns:
        List of chunked Document objects.
    """
    print_status("Splitting documents into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(documents)
    print_success(f"Created {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    return chunks


def create_vector_store(
    chunks: list,
    vectordb_dir: Path = VECTORDB_DIR,
) -> FAISS:
    """Generate embeddings and persist the FAISS vector store.

    Args:
        chunks: List of chunked Document objects.
        vectordb_dir: Path to save the FAISS index.

    Returns:
        The created FAISS vector store instance.
    """
    print_status("Generating embeddings via Google Gemini (this may take a moment)...")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
    )
    vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)

    # Ensure the output directory exists
    vectordb_dir.mkdir(parents=True, exist_ok=True)

    print_status("Saving vector database...")
    vector_store.save_local(str(vectordb_dir))

    print_success(f"Vector database saved to {vectordb_dir}")
    return vector_store


def run_ingestion() -> None:
    """Run the complete ingestion pipeline.

    Orchestrates: PDF loading → chunking → embedding → FAISS persistence.
    Displays progress messages throughout.
    """
    print()
    print_separator()
    print("  📂  DOCUMENT INGESTION PIPELINE")
    print_separator()
    print()

    # Validate data directory exists
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print_error(f"Data directory created at {DATA_DIR}")
        print("  Please add PDF files and run ingestion again.")
        sys.exit(1)

    # Step 1: Load PDFs
    documents = load_pdfs()

    # Step 2: Split into chunks
    chunks = split_documents(documents)

    # Step 3: Create vector store
    create_vector_store(chunks)

    print()
    print_success("Ingestion completed successfully! ✨")
    print()


# ── Allow running ingestion as a standalone script ───────────────────────────
if __name__ == "__main__":
    from src.config import validate_api_key

    validate_api_key()
    run_ingestion()
