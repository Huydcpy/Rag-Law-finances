import os
from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser
from llama_index.core.schema import Document

class LawAndFinanceParser:
    def __init__(self, chunk_size=512, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # NodeParser cho văn bản thông thường / Luật
        self.law_parser = SentenceSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        # NodeParser tối ưu cho BCTC dạng bảng / Markdown từ LlamaParse
        self.finance_parser = MarkdownNodeParser()

    def parse_law_document(self, text: str, doc_name: str = "luat.pdf"):
        """Xử lý văn bản Luật Doanh Nghiệp"""
        doc = Document(text=text, metadata={"source": doc_name, "domain": "Law"})
        nodes = self.law_parser.get_nodes_from_documents([doc])
        print(f"[*] Đã chunking Luật: {len(nodes)} nodes tạo ra.")
        return nodes

    def parse_finance_document(self, markdown_text: str, doc_name: str = "bctc.pdf"):
        """Xử lý Báo cáo tài chính (dạng Markdown từ LlamaParse)"""
        doc = Document(text=markdown_text, metadata={"source": doc_name, "domain": "Finance"})
        nodes = self.finance_parser.get_nodes_from_documents([doc])
        print(f"[*] Đã chunking BCTC: {len(nodes)} nodes tạo ra.")
        return nodes

if __name__ == "__main__":
    print("Module Parsing & Chunking sẵn sàng!")
