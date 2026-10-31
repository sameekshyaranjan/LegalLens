# LegalLens — AI Legal Assistant

An intelligent, terminal-based legal research assistant powered by **Retrieval-Augmented Generation (RAG)**. The system ingests legal PDF documents, indexes them into a local vector database, retrieves semantically relevant sections for user questions, and generates strictly grounded answers with document citations and page numbers using **Google Gemini**.

---

## Overview

Legal documents such as statutes, acts, contracts, and case files are lengthy, dense, and difficult to search quickly. Standard conversational AI models often hallucinate or fail to reference specific provisions accurately. 

**AI Legal Assistant** solves this problem by combining LangChain, Google Gemini embeddings, and FAISS vector search into a local RAG pipeline. It retrieves the exact sections relevant to a query and instructs the Gemini language model to answer solely based on that context, ensuring high factual accuracy and clear traceability to source documents.

---

## Key Features

- **PDF Ingestion & Processing**: Extracts text from PDF files placed in the `data/` directory and tracks source filenames and page numbers.
- **Semantic Chunking**: Splits documents into manageable passages using recursive character text splitting (500-character chunks with 100-character overlap) to preserve context.
- **Local Vector Storage**: Generates dense vector embeddings using Google Generative AI (`models/text-embedding-004`) and stores them locally with FAISS for fast similarity search.
- **Grounded Answer Generation**: Uses deterministic responses (`temperature=0.0`) with Google Gemini (`gemini-1.5-flash`), constrained by a strict system prompt to eliminate hallucinations and avoid unsupported legal advice.
- **Source Citations**: Automatically attributes every answer with deduplicated document names and page numbers.
- **Interactive Terminal Interface**: Continuous command-line REPL with automatic first-run ingestion detection and clean terminal formatting.

---

## Tech Stack

| Layer | Technology | Role |
|---|---|---|
| **Language** | Python 3.11+ | Core programming language |
| **Framework** | LangChain (`langchain`, `langchain-community`, `langchain-google-genai`) | RAG orchestration, prompt templates, and LLM chains |
| **LLM** | Google Gemini (Default: `gemini-1.5-flash`, configurable) | Context-grounded response generation |
| **Embeddings** | Google Generative AI Embeddings (`models/text-embedding-004`) | Semantic vector representation of document chunks |
| **Vector Database** | FAISS (`faiss-cpu`) | Local similarity search and index persistence |
| **Document Loader** | PyPDF (`pypdf`) | PDF reading and page extraction |
| **Environment** | python-dotenv | Loading API keys and environment configurations |

---

## Project Structure

```text
AI Legal Assistant/
├── data/                  # Directory for input legal PDF files
│   └── legal doc.pdf      # Example legal document
├── vectordb/              # Persisted FAISS vector index (auto-generated)
├── src/
│   ├── __init__.py        # Package initializer
│   ├── config.py          # Central configuration, paths, and constants
│   ├── ingest.py          # PDF loading, chunking, and embedding pipeline
│   ├── retriever.py       # FAISS index loader and top-K similarity search
│   ├── llm.py             # LLM setup and answer generation chain
│   ├── prompts.py         # System prompt and RAG prompt templates
│   └── utils.py           # Terminal formatting and display helpers
├── main.py                # Main CLI application entry point
├── architecture.md        # System design specifications & requirements
├── requirements.txt       # Project dependencies
├── .env.example           # Template for environment variables
└── README.md              # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python 3.11+** installed on your machine.
- A **Google Gemini API Key** (Free tier available at [Google AI Studio](https://aistudio.google.com/app/apikey)).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sameekshyaranjan/LegalLens.git
   cd LegalLens
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

Copy the example configuration file and add your Gemini API key:

```bash
cp .env.example .env
```

Open `.env` and set your credentials:

```env
# Required: Your Google Gemini API key from Google AI Studio
GEMINI_API_KEY=your-gemini-api-key-here

# Optional: Override default models if desired
# LLM_MODEL=gemini-1.5-flash
# EMBEDDING_MODEL=models/text-embedding-004
```

> **Security Note:** Never commit your `.env` file to version control. It is already included in `.gitignore`.

---

## Running the Project

### 1. Add Legal Documents
Place any legal PDF documents you want to query inside the `data/` folder:
```text
data/
└── your_document.pdf
```

### 2. Run the Application
Start the interactive assistant:
```bash
python main.py
```

- If no vector database is found in `vectordb/`, the application will ask if you want to run document ingestion automatically.
- Alternatively, you can run the ingestion pipeline separately at any time:
  ```bash
  python -m src.ingest
  ```

### 3. Example Terminal Interaction

```text
============================================================
  ⚖️   AI LEGAL ASSISTANT  (RAG-Powered)
============================================================

  ⏳ Loading vector database...
  ✅ System ready.

  Type your legal question below.
  Type 'exit', 'quit', or 'q' to quit.

============================================================
  Ask Legal Question:
  > What is Article 21?

============================================================
  📜  ANSWER
============================================================

  Article 21 of the Constitution of India guarantees the
  protection of life and personal liberty, stating that no
  person shall be deprived of their life or personal liberty
  except according to procedure established by law.

------------------------------------------------------------
  📎  SOURCES
------------------------------------------------------------

  1. legal doc.pdf | Page 32

============================================================
```

To exit the application, type `exit`, `quit`, or `q`.

---

## How It Works

```
Legal PDFs (data/) ──► Text Chunking ──► Gemini Embeddings ──► FAISS Vector DB
                                                                      │
User Question ─────────────────► Semantic Similarity Search (Top-3) ──┘
                                        │
                                        ▼
                             Retrieved Context + Prompt
                                        │
                                        ▼
                             Google Gemini (Temp=0)
                                        │
                                        ▼
                             Grounded Answer + Citations
```

1. **Ingestion & Indexing**: PDF files in `data/` are loaded via `PyPDFLoader` and split into 500-character chunks with 100-character overlap. Embeddings are generated via Google Generative AI (`models/text-embedding-004`) and saved into the local `vectordb/` directory using FAISS.
2. **Retrieval**: When a query is entered, `retriever.py` queries the FAISS index to fetch the top 3 (`TOP_K=3`) most semantically relevant text chunks.
3. **Prompt Augmentation**: The retrieved chunks are structured with source identifiers and page numbers into a strict legal assistant prompt template.
4. **Answer Generation**: The Gemini model synthesizes a concise, factual answer strictly from the retrieved text. If the answer is not present, it responds: *"Information not found in provided documents."*

---

## Future Improvements

- **Web & API Interfaces**: Expose the pipeline through a FastAPI backend and a Streamlit or React frontend.
- **Multi-Format Support**: Support additional file formats such as Word documents (`.docx`), plain text (`.txt`), and scanned PDFs via OCR.
- **Hybrid Retrieval**: Combine BM25 keyword matching with dense vector similarity to improve precision on specific section and statute numbers.
- **Conversation Memory**: Support follow-up legal queries and multi-turn reasoning within the same session.