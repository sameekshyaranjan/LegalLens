"""
prompts.py — Prompt Engineering

Defines the system prompt and builds the full chat prompt template
for the AI Legal Assistant. All prompting logic is isolated here.
"""

from langchain_core.prompts import ChatPromptTemplate

# ── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT: str = """You are an AI Legal Research Assistant.

Your role is to answer legal questions ONLY from the provided legal context.

Rules:
- Do not hallucinate.
- Do not invent laws, acts, sections, or judgments.
- If the information is not available in the provided context, say:
  "Information not found in provided documents."
- Do not provide personal legal advice.
- Maintain a professional and formal tone.
- Cite retrieved sources (document name, page number) whenever possible.
- Keep answers concise but informative.
- Structure your answers clearly with proper formatting.
"""

# ── Human Prompt Template ────────────────────────────────────────────────────
HUMAN_PROMPT: str = """Use the following legal context to answer the question.

--- LEGAL CONTEXT ---
{context}
--- END CONTEXT ---

Question: {question}

Provide a clear, well-structured answer based ONLY on the context above.
If the answer cannot be found in the context, state that clearly.
"""


def build_prompt() -> ChatPromptTemplate:
    """Build and return the chat prompt template for the RAG pipeline.

    Returns:
        ChatPromptTemplate: The assembled prompt with system and human messages.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", HUMAN_PROMPT),
        ]
    )
