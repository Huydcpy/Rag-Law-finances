import chromadb

from .parser import documents
from .chunker import split_documents

from ..embedding.embedding import embed_model

from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex

from llama_index.vector_stores.chroma import ChromaVectorStore

from src.configs.settings import CHROMA_PERSIST_DIR

nodes = split_documents(documents)

client = chromadb.PersistentClient(
    path=CHROMA_PERSIST_DIR
)

collection = client.get_or_create_collection(
    "law_finance"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

index = VectorStoreIndex(
    nodes=nodes,
    storage_context=storage_context,
    embed_model=embed_model,
)

print(f"Indexed {len(nodes)} chunks successfully.")