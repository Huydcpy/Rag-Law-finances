import os
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.query_engine import CitationQueryEngine

class LawFinanceEngine:
    def __init__(self, nodes, similarity_top_k=3, citation_chunk_size=512):
        print("[*] Đang khởi tạo Vector Index...")
        self.index = VectorStoreIndex(nodes)
        
        print("[*] Khởi tạo CitationQueryEngine...")
        self.query_engine = CitationQueryEngine.from_args(
            self.index,
            similarity_top_k=similarity_top_k,
            citation_chunk_size=citation_chunk_size,
        )

    def query(self, question: str):
        """Truy vấn dữ liệu và trả về câu trả lời kèm trích dẫn nguồn"""
        response = self.query_engine.query(question)
        return response

if __name__ == "__main__":
    print("Module Engine sẵn sàng!")
