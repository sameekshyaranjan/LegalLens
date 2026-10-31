# PRODUCT REQUIREMENTS DOCUMENT (PRD)

# AI Legal Assistant using RAG (Phase 1)

---

# 1. PROJECT OVERVIEW

Build a terminal-based AI Legal Assistant capable of answering legal questions from uploaded legal PDF documents using a Retrieval-Augmented Generation (RAG) pipeline.

The system must:
- ingest legal PDF documents
- split documents into semantic chunks
- generate embeddings
- store embeddings in a FAISS vector database
- retrieve relevant chunks for user queries
- generate grounded responses using Google Gemini LLM
- display answers with citations directly in terminal

This project is intended for a college major project Phase-1 demo.

The system should prioritize:
- simplicity
- modular architecture
- clean code
- explainability
- reliability
- low hallucination

DO NOT build frontend/UI/web app.
Everything must run completely in terminal.

---

# 2. PRIMARY OBJECTIVE

Demonstrate:
- Retrieval-Augmented Generation (RAG)
- Vector embeddings
- Semantic similarity search
- Context-grounded LLM responses
- AI-powered legal document querying

The project should appear technically strong during:
- viva
- review presentation
- project demo

---

# 3. TECH STACK

Use ONLY the following stack.

## Language
Python 3.11+

## Libraries
- langchain
- langchain-google-genai
- langchain-community
- faiss-cpu
- pypdf
- python-dotenv
- google-generativeai

## LLM
Google Gemini model (e.g. gemini-1.5-flash)

## Embeddings
GoogleGenerativeAIEmbeddings (models/text-embedding-004)

## Vector Database
FAISS

---

# 4. CORE FEATURES

## Feature 1 — PDF Ingestion

The system must:
- load PDF documents from `/data`
- extract text from all pages
- preserve metadata:
  - source filename
  - page number

---

## Feature 2 — Chunking

Use:
RecursiveCharacterTextSplitter

Requirements:
- chunk_size = 500
- chunk_overlap = 100

Chunks should preserve semantic continuity.

---

## Feature 3 — Embeddings

Generate embeddings using:
GoogleGenerativeAIEmbeddings

---

## Feature 4 — Vector Database

Store embeddings locally using FAISS.

Persist database to:
`/vectordb`

---

## Feature 5 — Retrieval

Use semantic similarity search.

Requirements:
- top_k = 3
- retrieve most relevant chunks

---

## Feature 6 — LLM Answer Generation

Use:
ChatGoogleGenerativeAI

Requirements:
- temperature = 0
- grounded responses only
- no hallucinations

Prompt rules:
- answer ONLY from retrieved context
- if answer unavailable:
  "Information not found in provided documents."
- do not provide personal legal advice

---

## Feature 7 — Terminal Interaction

The application must:
- run entirely in terminal
- continuously accept user queries
- support exit command

Example:

```bash
python main.py
```

Example interaction:

```text
Ask Legal Question:
> What is Article 21?
```

---

# 5. PROJECT STRUCTURE

Generate production-style folder structure.

```text
legal_assistant/
│
├── data/
│   └── constitution.pdf
│
├── vectordb/
│
├── src/
│   ├── ingest.py
│   ├── retriever.py
│   ├── llm.py
│   ├── prompts.py
│   ├── config.py
│   └── utils.py
│
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# 6. CODE QUALITY REQUIREMENTS

The code must:
- follow clean architecture
- use modular functions
- include comments
- use type hints
- handle errors gracefully
- avoid hardcoded values
- use environment variables

DO NOT generate monolithic code.

---

# 7. ENVIRONMENT VARIABLES

Use `.env`.

Variables:

```env
GEMINI_API_KEY=
```

---

# 8. README REQUIREMENTS

Generate professional README containing:
- project overview
- architecture
- setup instructions
- installation commands
- usage instructions
- sample queries
- explanation of RAG
- future scope

README should look professional enough for GitHub.

---

# 9. PROMPT ENGINEERING REQUIREMENTS

Create a dedicated `prompts.py`.

System prompt must:
- behave as AI legal research assistant
- avoid hallucination
- answer only from provided context
- refuse unsupported claims
- avoid personal legal advice
- maintain professional tone

---

# 10. OUTPUT FORMAT

Terminal output should look clean.

Example:

```text
==================================================
AI LEGAL ASSISTANT
==================================================

Ask Legal Question:
> What is Article 21?

==================================================
ANSWER
==================================================

Article 21 guarantees protection of life and
personal liberty...

==================================================
SOURCES
==================================================

1. constitution.pdf | Page 32
2. constitution.pdf | Page 33
```

---

# 11. NON-FUNCTIONAL REQUIREMENTS

The application should:
- run locally
- work offline after embeddings are created except LLM calls
- be easy to explain in viva
- beginner friendly
- avoid unnecessary abstractions

---

# 12. DO NOT INCLUDE

DO NOT:
- build frontend
- build authentication
- build PostgreSQL/MySQL databases
- use Docker
- use Kubernetes
- build APIs
- use LangGraph
- use AI agents
- use fine-tuning
- use Redis
- use cloud deployment
- use microservices

Keep Phase-1 minimal and stable.

---

# 13. FUTURE SCOPE SECTION

Mention future improvements:
- multi-PDF support
- case summarization
- legal precedent recommendation
- multilingual support
- voice assistant
- FastAPI backend
- Streamlit UI
- judge assistance system
- predictive legal analytics

---

# 14. CODING STYLE

Code should look like:
- senior software engineer wrote it
- production-quality starter project
- readable for college students
- easy to extend later

Prefer:
- explicit code
- clarity over cleverness
- maintainability

---

# 15. RAG PIPELINE FLOW

The architecture flow should be:

```text
Legal PDF
    ↓
PDF Loader
    ↓
Chunking
    ↓
Google Gemini Embeddings
    ↓
FAISS Vector Store
    ↓
Retriever
    ↓
Google Gemini LLM
    ↓
Grounded Legal Response
    ↓
Terminal Output
```

---

# 16. SYSTEM PROMPT REQUIREMENTS

Use a strong system prompt similar to:

```text
You are an AI Legal Research Assistant.

Your role is to answer legal questions ONLY from the provided legal context.

Rules:
- Do not hallucinate.
- Do not invent laws, acts, sections, or judgments.
- If information is unavailable, say:
  "Information not found in provided documents."
- Do not provide personal legal advice.
- Maintain a professional and formal tone.
- Cite retrieved sources whenever possible.
- Keep answers concise but informative.
```

---

# 17. INGESTION REQUIREMENTS

The ingestion pipeline should:
- load all PDFs from `/data`
- process multiple PDFs automatically
- create embeddings
- save FAISS index locally
- display ingestion progress in terminal

Example:

```text
Loading PDFs...
Splitting documents...
Generating embeddings...
Saving vector database...
Ingestion completed successfully.
```

---

# 18. RETRIEVAL REQUIREMENTS

Retriever should:
- use similarity search
- retrieve top 3 chunks
- preserve metadata
- return clean context

The retrieved context must be appended into the final LLM prompt.

---

# 19. ERROR HANDLING

Implement proper error handling for:
- missing API key
- missing PDFs
- empty vector database
- Gemini API failures
- invalid user input

Terminal errors should be clean and user friendly.

Example:

```text
ERROR: No PDF files found in /data
```

---

# 20. REQUIREMENTS.TXT

Generate a proper `requirements.txt`.

Expected packages:

```txt
langchain
langchain-google-genai
langchain-community
faiss-cpu
pypdf
python-dotenv
google-generativeai
```

---

# 21. README QUALITY

README must include:
- architecture explanation
- setup instructions
- example screenshots (optional placeholders)
- example legal questions
- future roadmap
- explanation of RAG
- explanation of vector embeddings

README should look professional enough for:
- GitHub portfolio
- college submission
- resume projects

---

# 22. SAMPLE QUESTIONS FOR TESTING

Include example questions:

```text
What is Article 21?
What are fundamental rights?
What is punishment for theft?
Explain Article 19.
What is right to equality?
```

---

# 23. PERFORMANCE REQUIREMENTS

The application should:
- respond within reasonable time
- avoid redundant embedding generation
- load vector DB efficiently
- support moderate-sized PDFs

---

# 24. ADVANCED ENGINEERING REQUIREMENTS

The generated project should follow:
- separation of concerns
- reusable utility functions
- configurable constants
- modular architecture
- extensibility for future phases

Ensure:
- ingestion logic is isolated
- retrieval logic is isolated
- prompting logic is isolated
- LLM interaction is isolated

The architecture should support future:
- API integration
- frontend integration
- multi-agent systems
- LangGraph migration
- cloud deployment

without major refactoring.

---

# 25. CODING STANDARDS

Use:
- meaningful variable names
- docstrings
- comments where necessary
- proper exception handling
- clean imports
- organized files

Avoid:
- spaghetti code
- giant functions
- repeated code
- hardcoded paths

---

# 26. TERMINAL UX REQUIREMENTS

The terminal experience should feel professional.

Example:

```text
==================================================
AI LEGAL ASSISTANT
==================================================

Loading vector database...
System ready.

Ask Legal Question:
> What is Article 21?
```

Responses should be formatted clearly with:
- headings
- spacing
- citations
- separators

---

# 27. SECURITY REQUIREMENTS

Ensure:
- API keys are loaded from `.env`
- `.env` is added to `.gitignore`
- secrets are never hardcoded

---

# 28. FINAL DELIVERABLES

Generate:
- complete source code
- modular architecture
- requirements.txt
- README.md
- .env.example
- working terminal-based RAG application

The generated code must run successfully after:
1. installing requirements
2. adding Gemini API key
3. placing PDFs inside `/data`
4. running ingestion
5. running `main.py`

Ensure:
- no broken imports
- no missing dependencies
- no placeholder code
- no incomplete functions

Everything should be executable and production-style.

---

# 29. FINAL INSTRUCTION TO CODEX

Act as a senior AI engineer and generate a complete production-quality Phase-1 AI Legal Assistant project.

The output must:
- be modular
- be executable
- be beginner-friendly
- follow clean architecture
- use LangChain correctly
- use Google Gemini correctly
- use FAISS correctly
- contain professional documentation
- contain no incomplete implementations

Focus on:
- reliability
- simplicity
- explainability
- clean engineering

Do not overengineer the solution.
Keep it minimal, stable, and extensible.