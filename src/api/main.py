import sys
from pathlib import Pathi
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import json
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Import ChromaVectorStore và LlamaIndex components
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.query_engine import CitationQueryEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAG_Backend")

# Biến toàn cục lưu query engine
query_engine_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global query_engine_instance
    logger.info("⏳ Đang kết nối Chroma DB và khởi tạo CitationQueryEngine...")
    try:
    
        # 1. Khởi tạo Chroma Client trỏ tới thư mục lưu trữ DB (thường là ./chroma_db)
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # 2. Lấy Collection do Thành viên 1 & 2 đã khởi tạo (ví dụ: 'law_finance_docs')
        chroma_collection = chroma_client.get_or_create_collection("law_finance_docs")
        
        # 3. Tạo Vector Store & Index từ Chroma
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # 4. Khởi tạo CitationQueryEngine để tự động trích dẫn nguồn
        query_engine_instance = CitationQueryEngine.from_args(
            index=index,
            similarity_top_k=3,
            citation_chunk_size=512
        )
        logger.info("✅ Khởi tạo CitationQueryEngine từ Chroma DB thành công!")
        
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi tạo Engine từ Chroma DB: {str(e)}")
        # Fallback cảnh báo nếu chưa chạy ingestion pipeline để tạo chroma_db
        logger.warning("⚠️ Hãy chắc chắn Thành viên 1 đã chạy script Ingestion để tạo Chroma DB!")
        
    yield
    logger.info("🛑 Đang đóng dịch vụ Backend...")

app = FastAPI(
    title="RAG Domain-Specific QA API",
    description="Backend API cho hệ thống Trợ lý AI Luật & Tài chính",
    version="1.0.0",
    lifespan=lifespan
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "engine_ready": query_engine_instance is not None
    }

async def generate_rag_response(query: str):
    """
    Generator stream dữ liệu phản hồi dạng SSE, trích xuất nguồn từ CitationQueryEngine
    """
    try:
        if query_engine_instance is None:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Engine/Chroma DB chưa sẵn sàng. Vui lòng kiểm tra lại dữ liệu vector.'})}\n\n"
            return

        # 1. Gọi truy vấn Async từ CitationQueryEngine
        response = await query_engine_instance.aquery(query)

        # 2. Bóc tách nguồn trích dẫn từ source_nodes
        sources = []
        if hasattr(response, "source_nodes"):
            for node in response.source_nodes:
                metadata = node.node.metadata or {}
                sources.append({
                    "file_name": metadata.get("file_name", metadata.get("filename", "Văn bản gốc")),
                    "page": metadata.get("page_label", metadata.get("page", "N/A")),
                    "section": metadata.get("section", "N/A"),
                    "text": node.node.get_content()[:200] + "..."  # Xem trước 200 ký tự
                })

        # Gửi dữ liệu nguồn trích dẫn về Frontend trước để cập nhật Sidebar
        yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"
        await asyncio.sleep(0.01)

        # 3. Stream nội dung câu trả lời
        if hasattr(response, "async_response_gen"):
            async for token in response.async_response_gen():
                yield f"data: {json.dumps({'type': 'content', 'data': token})}\n\n"
        else:
            response_text = str(response)
            for word in response_text.split(" "):
                yield f"data: {json.dumps({'type': 'content', 'data': word + ' '})}\n\n"
                await asyncio.sleep(0.02)

        # 4. Gửi tín hiệu hoàn thành
        yield f"data: {json.dumps({'type': 'end'})}\n\n"

    except Exception as e:
        logger.error(f"Lỗi khi xử lý RAG Stream: {str(e)}")
        yield f"data: {json.dumps({'type': 'error', 'message': f'Lỗi hệ thống: {str(e)}'})}\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống")

    return StreamingResponse(
        generate_rag_response(request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
