from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import CitationQueryEngine

class LawFinanceEngine:
    def __init__(self, index_or_nodes, similarity_top_k=5, citation_chunk_size=512):
        print("[*] Đang khởi tạo Vector Index...")
        if isinstance(index_or_nodes, VectorStoreIndex):
            self.index = index_or_nodes
        else:
            self.index = VectorStoreIndex(index_or_nodes)
        
        print("[*] Khởi tạo CitationQueryEngine...")
        self.query_engine = CitationQueryEngine.from_args(
            self.index,
            similarity_top_k=similarity_top_k,
            citation_chunk_size=citation_chunk_size,
        )

    def query(self, question: str):
        """Truy vấn đồng bộ (Sync)"""
        return self.query_engine.query(question)

    async def aquery(self, question: str):
        """Truy vấn bất đồng bộ (Async)"""
        return await self.query_engine.aquery(question)

if __name__ == "__main__":
    print("Module Engine sẵn sàng!")
