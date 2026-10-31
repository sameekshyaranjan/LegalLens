"""
config.py — Centralized Configuration

Loads environment variables and defines all project-wide constants.
All configurable values live here — nothing is hardcoded elsewhere.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ── Load Environment Variables ───────────────────────────────────────────────
load_dotenv(override=True)

# ── Paths ────────────────────────────────────────────────────────────────────
# Project root is one level above src/
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
VECTORDB_DIR: Path = PROJECT_ROOT / "vectordb"

# ── Google Gemini Configuration ─────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")
LLM_TEMPERATURE: float = 0.0

# ── Chunking Configuration ──────────────────────────────────────────────────
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 100

# ── Retrieval Configuration ─────────────────────────────────────────────────
TOP_K: int = 3


def validate_api_key() -> None:
    """Validate that the Gemini API key is configured.

    Raises:
        SystemExit: If the API key is missing or still set to the placeholder.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY in ("your-gemini-api-key-here", "your-google-api-key-here"):
        print("\n❌ ERROR: GEMINI_API_KEY (or GOOGLE_API_KEY) is not set.")
        print("   Please create a .env file with your API key:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your Gemini API key from Google AI Studio (https://aistudio.google.com/app/apikey)")
        sys.exit(1)
