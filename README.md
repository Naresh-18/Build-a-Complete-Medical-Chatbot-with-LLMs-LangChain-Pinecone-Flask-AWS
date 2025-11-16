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

---

# Indexing documents (create Pinecone vectors)
1. Add your PDF or research files into the ```data/``` or ```research/``` folder.
2. Run the indexer:
   ```bash
   python store_index.py
   ```
```store_index.py``` will:
- Load PDFs
- Extract text and clean it
- Split text into chunks
- Compute embeddings
- Upsert vectors into the Pinecone index
  
Make sure ```.env``` is configured before running.

---

# Running the Flask App (Local)
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8080
```
Open ```http://localhost:8080``` to use the minimal chat UI. The app sends queries to the RAG chain which retrieves relevant docs and queries the LLM.

---

# How the RAG chain works
1. Retriever: the app queries Pinecone for the top-```k``` similar chunks for the user prompt.
2. Prompting: retrieved chunks are injected into a system prompt (see ```prompts``` inside the code).
3. LLM: the chain calls ```langchain_openai.ChatOpenAI``` (configured with model name) which hits OpenRouter/OpenAI.
4. Answer: the model returns a concise, context-aware medical answer.

Tip: Update your system prompt to gracefully handle empty context (greetings vs medical Qs).

---

# AWS CI/CD Deployment with GitHub Actions

Follow these steps to automate build, push and deployment of your Dockerized app to AWS using GitHub Actions and a self-hosted runner on an EC2 instance.

## 1. Prepare AWS
  1. Login to the AWS Console.
  2. Create an IAM user for deployment with these policies:
     - ```AmazonEC2ContainerRegistryFullAccess```
     - ```AmazonEC2FullAccess```

## 2. Create ECR repository
  1. Create an ECR repository to store your Docker image (example URI):
     ```bash
     315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot
     ```
Save the URI — you'll use it in GitHub secrets and your CI workflow. 

## 3. Create and configure EC2 (Ubuntu)
 1. Launch an EC2 Ubuntu instance (this will serve as a self-hosted runner and runtime host).
 2. (Optional) Update packages:
    ```bash
    sudo apt-get update -y
    sudo apt-get upgrade -y
    ```
 3. Install Docker (required):
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    newgrp docker
    ```
 4. (Optional) Test Docker:
    ```bash
    docker run hello-world
    ```

## 4. Configure EC2 as a self-hosted GitHub Actions runner
1. In your GitHub repository: ```Settings -> Actions -> Runners -> New self-hosted runner.```
2. Choose the OS and follow the displayed commands to register the runner on your EC2 instance. Run each command in the EC2 shell to install and start the runner.

## 5. CI/CD workflow (high-level)
Your GitHub Actions workflow should:
1. Build the Docker image of your source code.
2. Authenticate with ECR and push the image to the ECR repo.
3. (Optional) SSH / use the self-hosted runner to pull the image on the EC2 host.
4. Run the Docker container on the EC2 host.

A typical workflow uses these steps: ```checkout```, ```set up QEMU```/```Docker buildx``` (if needed), ```build image```, ```login to AWS ECR```, ```push image```, and ```deploy``` on EC2 (or let the self-hosted runner pull and run).

## 6. Required GitHub Secrets
Add these secrets to your GitHub repository (```Settings -> Secrets -> Actions```):
- ```AWS_ACCESS_KEY_ID```
- ```AWS_SECRET_ACCESS_KEY```
- ```AWS_DEFAULT_REGION``` (example: ```us-east-1```)
- ```ECR_REPO``` (the ECR repository URI)
- ```PINECONE_API_KEY```
- ```OPENAI_API_KEY``` (OpenRouter/OpenAI-compatible key)

## 7. Example policies and notes
- Ensure the IAM user has ```AmazonEC2ContainerRegistryFullAccess``` and ```AmazonEC2FullAccess``` or a more limited set of permissions suitable for your environment.
- The self-hosted runner must be secured (restrict inbound ports, use an SSH key and security groups). Use AWS Secrets Manager to protect long-lived credentials for production.

By following this README, you will clearly understand the motivation behind the medical chatbot project, the full technology stack used, key implementation highlights, how to set up and run the system locally, and how to deploy it using AWS CI/CD with GitHub Actions. Additionally, the README outlines best practices, troubleshooting tips, and areas for potential enhancement—helping you extend, optimize, or productionize the chatbot with confidence.
