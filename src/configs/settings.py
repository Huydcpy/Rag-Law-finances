import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Embedding
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-m3")

# LLM
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "qwen2.5:7b")

# Vector Store
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(ROOT_DIR / "data" / "chroma_db"))

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Retrieval
TOP_K = int(os.getenv("TOP_K", "5"))
