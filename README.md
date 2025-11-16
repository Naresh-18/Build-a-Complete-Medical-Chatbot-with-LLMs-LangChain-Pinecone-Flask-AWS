# Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS
Build a full‑stack, document‑driven medical chatbot using large language models (via OpenRouter/OpenAI compatible APIs), LangChain for RAG flows, Pinecone for vector search, Flask as the API/serving layer, and AWS for deployment. This repository contains code for indexing research PDFs, building a retrieval-augmented generator, and serving a web UI.

---

# Key Components
  - ```app.py``` — Flask app that exposes the chatbot API and web UI (templates/static).
  - ```store_index.py``` — Script to load documents (PDFs), split text, embed, and upsert into Pinecone index.
  - ```src/``` — Helper utilities for PDF extraction, text cleaning, splitting, and embeddings.
  - ```research/``` — Example or source research documents (PDFs / notebooks) used to build the corpus.
  - ```templates/``` & ```static``` — Frontend files for the minimal web UI.
  - ```requirements.txt``` — Python dependencies used by the project.
  - ```DockerFile``` — Containerization instructions for running the app in Docker.

---

# Features
  - Document-driven Question Answering (RAG): answer medical queries using indexed documents.
  - Pinecone vector index for fast semantic search.
  - LangChain chains to combine retrieval and LLM generation.
  - Flask API + simple web UI to test queries.
  - Configurable to use OpenRouter (DeepSeek) or OpenAI-compatible models.

---

# Prerequisites
  - Python 3.9+ (virtualenv recommended)
  - Pinecone account and API key
  - OpenRouter/OpenAI-compatible API key (or any OpenAI-compatible endpoint)
  - AWS account for deployment

---

# Installation
```bash
# create venv and activate
python -m venv venv
source venv/bin/activate # on Windows: venv\Scripts\activate

# install deps
pip install -r requirements.txt
```

---

# Environment variables
Create a ```.env``` file in the project root with the following values:
```bash
# OpenRouter (or OpenAI-compatible) key
OPENAI_API_KEY=your_openrouter_or_openai_key_here
# Point LangChain/OpenAI-compatible client to OpenRouter
OPENAI_API_BASE=https://openrouter.ai/api/v1

# Pinecone key and environment/region
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east1-gcp # example (use your Pinecone env)

# App options
FLASK_ENV=development
INDEX_NAME=medical-chatbot
```
Note: If you use OpenAI directly, you can omit ```OPENAI_API_BASE``` or set it to the OpenAI default. For OpenRouter/DeepSeek, set ```OPENAI_API_BASE``` to ```https://openrouter.ai/api/v1``` and choose the appropriate model in the code (e.g. ```deepseek/deepseek-chat```).
