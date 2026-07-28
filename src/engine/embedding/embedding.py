from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.configs.settings import EMBEDDING_MODEL_NAME

embed_model = HuggingFaceEmbedding(
    model_name=EMBEDDING_MODEL_NAME
)