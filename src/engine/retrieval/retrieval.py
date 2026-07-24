import chromadb

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex

client = chromadb.PersistentClient(
    path="data/chroma_db"
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
    similarity_top_k=5
)