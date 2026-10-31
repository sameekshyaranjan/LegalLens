"""
retriever.py — Vector Store Retrieval

Loads the persisted FAISS vector store and retrieves the most
relevant document chunks for a given query using similarity search.
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import EMBEDDING_MODEL, GEMINI_API_KEY, TOP_K, VECTORDB_DIR


def load_vector_store(vectordb_dir: Path = VECTORDB_DIR) -> FAISS:
    """Load the persisted FAISS vector store from disk.

    Args:
        vectordb_dir: Path to the saved FAISS index directory.

    Returns:
        The loaded FAISS vector store instance.

    Raises:
        FileNotFoundError: If the vector database directory does not exist.
    """
    if not vectordb_dir.exists():
        raise FileNotFoundError(
            f"Vector database not found at {vectordb_dir}. "
            "Please run ingestion first: python -m src.ingest"
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
    )
    vector_store = FAISS.load_local(
        str(vectordb_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vector_store


def retrieve_relevant_chunks(
    vector_store: FAISS,
    query: str,
    top_k: int = TOP_K,
) -> list:
    """Retrieve the most relevant document chunks for a query.

    Uses FAISS similarity search to find the closest chunks
    to the user's question.

    Args:
        vector_store: The loaded FAISS vector store.
        query: The user's legal question.
        top_k: Number of top results to retrieve.

    Returns:
        List of LangChain Document objects with metadata.
    """
    results = vector_store.similarity_search(query, k=top_k)
    return results
