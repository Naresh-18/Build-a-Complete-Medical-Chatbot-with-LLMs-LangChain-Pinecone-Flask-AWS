# 0. prerequisites
# pip install python-dotenv pinecone-client langchain-pinecone  # etc.

from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# 1. load .env early
load_dotenv()

# 2. read keys (do not blindly set os.environ to None)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")   # this is your OpenRouter key

# 3. validate keys and set environment safely
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found. Add it to your .env (PINECONE_API_KEY=...)")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Add your OpenRouter API key to .env (OPENAI_API_KEY=...)")

# Only set env vars when values are present (safe)
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# IMPORTANT: tell LangChain/OpenAI-compatible clients to use OpenRouter base
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"


# 4. your document/extraction pipeline (unchanged)
extracted_data = load_pdf_file(data="data/")
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

# 5. embeddings - ensure this returns a LangChain-compatible embedding object
embeddings = download_hugging_face_embeddings()  # your helper; ensure embedding.dim == 384

# -- quick check: if your embedding object exposes dimension, validate it --
try:
    # many HF wrappers have .embed_query or metadata; this is a gentle check
    sample_vector = embeddings.embed_query("hello world")
    dim = len(sample_vector)
    print("Embedding dimension detected:", dim)
    if dim != 384:
        print("Warning: embedding dimension != 384. Adjust Pinecone index dimension accordingly.")
except Exception as e:
    print("Could not auto-check embedding dimension:", e)
    # proceed but ensure you know your embedding dimension


# 6. Pinecone setup
pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)

index_name = "medical-chatbot"  # change if desired

# If the index exists with a different dimension, creation will fail — be careful
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,  # set this to your embedding dim if different
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)

# 7. create vector store from documents
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

print("Pinecone vectorstore ready.")
