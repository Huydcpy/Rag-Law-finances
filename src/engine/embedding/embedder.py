from src.configs.settings import EMBEDDING_MODEL_NAME


def get_embed_model():
    from llama_index.core import Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    embed_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL_NAME,
        max_length=8192,
        trust_remote_code=True,
        device="cpu",
    )
    Settings.embed_model = embed_model
    return embed_model
