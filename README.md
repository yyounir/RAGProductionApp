<div align="center">
  
  # 🗃️ Ask Filebot - RAG AI Chatbot

  **A basic retrieval-augmented generation (RAG) AI prototype into a production-ready application with Gemini API. Uses the inngest orchestration platform for rate-limiting, observability, and automated retries, and PDF loading / storage layer with Qdrant.**
  
  ![Python](https://img.shields.io/badge/Python-000000.svg?style=flat&logo=python) 
  ![Streamlit](https://img.shields.io/badge/Streamlit-000000.svg?style=flat&logo=Streamlit)
  ![FastAPI](https://img.shields.io/badge/Fast_API-000000.svg?style=flat&logo=fastapi)
  ![Qdrant](https://img.shields.io/badge/Qdrant-000000.svg?style=flat&logo=qdrant)
  ![RAG](https://img.shields.io/badge/RAG-000000.svg?style=flat&logo=rag)
  ![Gemini API](https://img.shields.io/badge/Gemini_API-000000.svg?style=flat&logo=embeddings)
  ![Inngest](https://img.shields.io/badge/Ingest-000000.svg?style=flat&logo=Inngest)
  ![Fault-Tolerant](https://img.shields.io/badge/Fault--Tolerant-000000.svg?style=flat&logo=Inngest)
</div>

## 📖 About this Project
I have developed a production-ready retrieval-augmented generation (RAG) AI agent in Python, which focuses on moving beyond simple scripts to robust architecture suitable for real-world deployment.

## 🛠️ Technologies Used
- Frontend: Streamlit
- Languages: Python
- Frameworks: FastAPI, Qdrant Vector Database, RAG, Ingest
- AI Model: Gemini 2.5 Flash

## ⭐ Key Features
- **Orchestration & Observability:** The core of this production-grade approach uses Inngest, which is used to manage workflow orchestration. It provides features such as automatic retries, logging, and performance tracking for each step of the AI agent 
- **Vector Database:** Utilizes Qdrant to store document embeddings, allows the AI to efficiently search and retrieve relevant data from your uploaded sites.
- **Data Ingestion:** Llamaindex is used to load, parse, and chunk PDF documents, turning them into a format the model can reason about based on the user's prompt.
- **AI Engine:** Uses Gemini 2.5 Flash model as a core LLM for answering questions based on the retrieved content.
- **Frontend:** A simple, interactive interface built with streamlit, allowing users to chat with their documents.
- **Fault-Tolerant:** Wraps the operations in "steps", the application becomes more stable, and uses concurrency controls to your API functions to prevent abuse and exceeding rate limits to the AI chatbot.

## 📝 Prerequisites
- Node.js (v20.19.0 or higher recommended)
- npm or yarn
- Docker (optional, for containerized deployment)

## 🚀 Server Setup
This repository provides a minimal, production-minded Retrieval-Augmented Generation (RAG) demo using Google Gemini, Inngest for orchestration, and Qdrant for vector storage. The instructions below get you a working local environment for development and testing.

## 💻 Supported platforms
- Local development (recommended): Windows / macOS / Linux
- Containerized: Docker (useful for Qdrant or Inngest local dev)

---

### 1. Python environment

Requirements: Python 3.13+ is required (see `pyproject.toml`). Create and activate a virtual environment:

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Upgrade pip and install the project dependencies using the included `pyproject.toml`:

```bash
python -m pip install --upgrade pip setuptools build
python -m pip install -e .
```

If you prefer a requirements file workflow, you can generate one from the installed environment.

### 2. Configuration
Create a `.env` file in the project root to store secrets and environment overrides. Minimal required values:

```
GEMINI_API_KEY=your_gemini_api_key_here
# Optional, override defaults as needed
INNGEST_API_BASE=http://127.0.0.1:8288/v1
QDRANT_URL=http://127.0.0.1:6333
```

Notes:
- `GEMINI_API_KEY` is required to call the Gemini model. Do not commit real keys to source control.
- `INNGEST_API_BASE` is used by the Streamlit UI to poll the Inngest dev API; the default points to a local Inngest instance.
- `QDRANT_URL` can point to a local Qdrant instance (the code defaults to `http://localhost:6333`).

### 3. Run prerequisites (optional but recommended)
- Qdrant (vector DB) quick start with Docker:

```bash
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
```

- Inngest local dev server (optional): follow Inngest docs or run any local dev mode if available. The Streamlit UI expects the Inngest API at `INNGEST_API_BASE`.

---

### 4. Running the application locally

1. Start the API (FastAPI + Inngest functions):

```bash
uvicorn main:app --reload --port 8000
```
```
uv run uvicorn main:app
```

2. In a separate terminal, start the Streamlit frontend:

```bash
uv run streamlit run .\streamlit_app.py
```

3. Open the Streamlit UI (usually at `http://localhost:8501`) to upload PDFs and ask questions.

### Workflow overview
- Upload a PDF via the Streamlit UI — this saves the file to `uploads/` and emits an Inngest event.
- Inngest triggers the `rag_ingest_pdf` workflow (`main.py`), which:
  - Loads and chunks the PDF (`data_loader.py`).
  - Calls Gemini to embed chunks (`embed_texts`).
  - Upserts vectors into Qdrant (`vector_db.py`).
- When querying, the UI emits a `rag/query_pdf_ai` event; Inngest runs `rag_query_pdf_ai`, which:
  - Embeds the user question, searches Qdrant for similar chunks, and calls Gemini to generate an answer limited to the retrieved context.

### Helpful commands

- Activate environment (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

- Install/update dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

- Run FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

- Run Streamlit UI:

```bash
streamlit run streamlit_app.py
```

### Environment variables reference
- `GEMINI_API_KEY` (required): API key for Google Gemini model.
- `INNGEST_API_BASE` (optional): URL for Inngest API (default `http://127.0.0.1:8288/v1`).
- `QDRANT_URL` (optional): Qdrant HTTP endpoint (default `http://localhost:6333`).

## ⚙️ Troubleshooting
- If Gemini calls fail: verify `GEMINI_API_KEY` and network access.
- If vector searches return empty results: confirm Qdrant is running and the collection `docs` exists; re-run an ingestion.
- Common port conflicts: change ports for Qdrant, FastAPI, or Streamlit as needed.

---

### Development notes
- Code entrypoints:
  - API + workflows: `main.py`
  - PDF ingestion & embedding: `data_loader.py`
  - Vector storage helper: `vector_db.py`
  - Streamlit frontend: `streamlit_app.py`

## 👥 Contributing
- Open issues or PRs for bugs or improvements. Follow standard Python packaging and run the app locally to test changes.

<div align="center">

## Contact
Have a project in mind? I'd love to hear about it! Check out my other work here!

[![Portfolio](https://img.shields.io/badge/My%20Portfolio-002500.svg?style=for-the-badge&logo=instatus&logoColor=white)](https://yyportfolio-xi.vercel.app/) [![LinkedIn](https://img.shields.io/badge/LinkedIn-002500.svg?style=for-the-badge&logo=instatus&logoColor=white)](https://www.linkedin.com/in/yasir-younus-91551a281) [![Gmail](https://img.shields.io/badge/Email-002500?style=for-the-badge&logo=gmail&logoColor=white)](mailto:yyproton168@gmail.com)
</div>