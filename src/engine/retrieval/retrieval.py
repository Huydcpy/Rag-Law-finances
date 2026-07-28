import chromadb

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex

from src.configs.settings import CHROMA_PERSIST_DIR, TOP_K

client = chromadb.PersistentClient(
    path=CHROMA_PERSIST_DIR
)

collection = client.get_collection(
    "law_finance"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

index = VectorStoreIndex.from_vector_store(
    vector_store
)

retriever = index.as_retriever(
    similarity_top_k=TOP_K
)