from llama_index.core.node_parser import SentenceSplitter

from src.configs.settings import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents):
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    return splitter.get_nodes_from_documents(documents)