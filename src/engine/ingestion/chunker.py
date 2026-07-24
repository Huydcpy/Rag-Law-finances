from llama_index.core.node_parser import SentenceSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def split_documents(documents):
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    return splitter.get_nodes_from_documents(documents)