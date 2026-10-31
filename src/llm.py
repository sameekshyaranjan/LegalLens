"""
llm.py — LLM Interaction Layer

Initializes the ChatGoogleGenerativeAI model and generates grounded answers
using retrieved context and the prompt template.
"""

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GEMINI_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from src.prompts import build_prompt


def get_llm() -> ChatGoogleGenerativeAI:
    """Initialize and return the ChatGoogleGenerativeAI language model.

    Returns:
        Configured ChatGoogleGenerativeAI instance with temperature=0
        for deterministic, grounded responses.
    """
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        google_api_key=GEMINI_API_KEY,
    )


def generate_answer(query: str, retrieved_docs: list) -> str:
    """Generate a grounded answer using the LLM and retrieved context.

    Builds the prompt from retrieved documents and the user's question,
    then invokes the LLM to produce a response.

    Args:
        query: The user's legal question.
        retrieved_docs: List of LangChain Document objects from the retriever.

    Returns:
        The LLM-generated answer as a string.
    """
    # Build context string from retrieved documents
    context_parts: list[str] = []
    for i, doc in enumerate(retrieved_docs, start=1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        context_parts.append(
            f"[Source {i}: {source}, Page {page}]\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    # Build the prompt chain
    prompt = build_prompt()
    llm = get_llm()
    chain = prompt | llm

    # Invoke the chain
    response = chain.invoke({"context": context, "question": query})

    return response.content
