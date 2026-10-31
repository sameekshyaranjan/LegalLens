"""
main.py — AI Legal Assistant Entry Point

Terminal-based interactive application that:
  1. Loads the FAISS vector database
  2. Accepts user legal questions in a loop
  3. Retrieves relevant document chunks
  4. Generates grounded answers via Google Gemini LLM
  5. Displays answers with source citations
"""

import sys

from src.config import validate_api_key, VECTORDB_DIR
from src.ingest import run_ingestion
from src.llm import generate_answer
from src.retriever import load_vector_store, retrieve_relevant_chunks
from src.utils import (
    print_answer,
    print_error,
    print_header,
    print_separator,
    print_sources,
    print_status,
    print_success,
    print_welcome,
)


# ── Exit Commands ────────────────────────────────────────────────────────────
EXIT_COMMANDS: set[str] = {"exit", "quit", "q"}


def initialize_system() -> object:
    """Initialize the system: validate config and load vector store.

    If the vector database does not exist, offers to run ingestion first.

    Returns:
        The loaded FAISS vector store.
    """
    # Validate API key
    validate_api_key()

    # Check if vector database exists
    if not VECTORDB_DIR.exists() or not any(VECTORDB_DIR.iterdir()):
        print()
        print_status("Vector database not found.")
        print()
        response = input("  Would you like to run document ingestion now? (y/n): ").strip().lower()

        if response in ("y", "yes"):
            run_ingestion()
        else:
            print()
            print("  To ingest documents, run:")
            print("    python -m src.ingest")
            print()
            sys.exit(0)

    # Load vector store
    print_status("Loading vector database...")

    try:
        vector_store = load_vector_store()
        print_success("System ready.")
        return vector_store
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to load vector database: {e}")
        sys.exit(1)


def handle_query(vector_store: object, query: str) -> None:
    """Process a single user query through the RAG pipeline.

    Args:
        vector_store: The loaded FAISS vector store.
        query: The user's legal question.
    """
    try:
        # Step 1: Retrieve relevant chunks
        retrieved_docs = retrieve_relevant_chunks(vector_store, query)

        if not retrieved_docs:
            print_answer("No relevant information found in the documents.")
            return

        # Step 2: Generate answer using LLM
        answer = generate_answer(query, retrieved_docs)

        # Step 3: Display answer
        print_answer(answer)

        # Step 4: Display sources
        sources = []
        for doc in retrieved_docs:
            sources.append({
                "source": doc.metadata.get("source", "Unknown"),
                "page": str(doc.metadata.get("page", "N/A")),
            })
        print_sources(sources)

    except Exception as e:
        print_error(f"Failed to process query: {e}")


def main() -> None:
    """Main application loop.

    Initializes the system and runs the interactive question-answer loop.
    """
    # Display header
    print_header()

    # Initialize
    vector_store = initialize_system()

    # Welcome message
    print_welcome()

    # Interactive loop
    while True:
        try:
            print_separator()
            query = input("  Ask Legal Question:\n  > ").strip()

            # Check for exit commands
            if query.lower() in EXIT_COMMANDS:
                print()
                print("  👋 Thank you for using AI Legal Assistant. Goodbye!")
                print()
                break

            # Skip empty queries
            if not query:
                print_error("Please enter a valid question.")
                continue

            # Process the query
            handle_query(vector_store, query)

        except KeyboardInterrupt:
            print()
            print()
            print("  👋 Session interrupted. Goodbye!")
            print()
            break
        except EOFError:
            print()
            break


# ── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
