from src.configs.settings import CHROMA_PERSIST_DIR, LLM_MODEL_NAME, OLLAMA_BASE_URL, TOP_K
from src.engine.embedding.embedder import get_embed_model


def get_rag_engine():
    import chromadb
    from llama_index.core import VectorStoreIndex, Settings
    from llama_index.llms.ollama import Ollama
    from llama_index.vector_stores.chroma import ChromaVectorStore

    embed_model = get_embed_model()

    llm = Ollama(
        model=LLM_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        request_timeout=600.0,
    )
    Settings.llm = llm

    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    collection = client.get_or_create_collection("law_finance")
    vector_store = ChromaVectorStore(chroma_collection=collection)

    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=TOP_K,
    )

    return query_engine
