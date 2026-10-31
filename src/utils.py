"""
utils.py — Terminal Display Utilities

Provides clean, professional terminal formatting for the legal assistant.
All print/display logic is isolated here for easy customization.
"""

# ── Constants ────────────────────────────────────────────────────────────────
SEPARATOR: str = "=" * 60
THIN_SEPARATOR: str = "-" * 60


def print_header() -> None:
    """Display the application header banner."""
    print()
    print(SEPARATOR)
    print("  ⚖️   AI LEGAL ASSISTANT  (RAG-Powered)")
    print(SEPARATOR)
    print()


def print_separator() -> None:
    """Print a visual separator line."""
    print(SEPARATOR)


def print_status(message: str) -> None:
    """Print a status/progress message.

    Args:
        message: The status text to display.
    """
    print(f"  ⏳ {message}")


def print_success(message: str) -> None:
    """Print a success message.

    Args:
        message: The success text to display.
    """
    print(f"  ✅ {message}")


def print_error(message: str) -> None:
    """Print a formatted error message.

    Args:
        message: The error text to display.
    """
    print(f"\n  ❌ ERROR: {message}\n")


def print_answer(answer: str) -> None:
    """Display the LLM-generated answer in a formatted block.

    Args:
        answer: The answer text from the LLM.
    """
    print()
    print(SEPARATOR)
    print("  📜  ANSWER")
    print(SEPARATOR)
    print()
    print(f"  {answer}")
    print()


def print_sources(sources: list[dict[str, str]]) -> None:
    """Display source citations from retrieved chunks.

    Args:
        sources: List of dicts with 'source' and 'page' keys.
    """
    print(THIN_SEPARATOR)
    print("  📎  SOURCES")
    print(THIN_SEPARATOR)
    print()

    if not sources:
        print("  No source information available.")
    else:
        # Deduplicate sources while preserving order
        seen: set[str] = set()
        index = 1
        for src in sources:
            source_file = src.get("source", "Unknown")
            page = src.get("page", "N/A")
            key = f"{source_file}|{page}"
            if key not in seen:
                seen.add(key)
                print(f"  {index}. {source_file} | Page {page}")
                index += 1

    print()
    print(SEPARATOR)
    print()


def print_welcome() -> None:
    """Display the welcome message after system initialization."""
    print()
    print("  Type your legal question below.")
    print("  Type 'exit', 'quit', or 'q' to quit.")
    print()
