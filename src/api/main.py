import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from src.engine.generation.engine import get_rag_engine

app = FastAPI(title="RAG Law & Finance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

rag_engine = None

def ensure_engine():
    global rag_engine
    if rag_engine is None:
        rag_engine = get_rag_engine()
    return rag_engine

async def generate_rag_response(query: str):
    try:
        engine = ensure_engine()
        if hasattr(engine, "aquery"):
            response_obj = await engine.aquery(query)
        else:
            response_obj = await run_in_threadpool(engine.query, query)
        
        # 2. Bóc tách Nguồn trích dẫn (Source Nodes)
        sources = []
        if hasattr(response_obj, "source_nodes") and response_obj.source_nodes:
            for node in response_obj.source_nodes:
                metadata = node.node.metadata or {}
                sources.append({
                    "file_name": metadata.get("file_name", "Tài liệu"),
                    "page": metadata.get("page_label", metadata.get("page", 1)),
                    "section": metadata.get("section", "Trích đoạn"),
                    "text": node.node.get_content()[:200] + "..." # Preview ngắn
                })
        
        # Gửi Nguồn trích dẫn sang Streamlit UI trước
        yield f"data: {json.dumps({'type': 'sources', 'data': sources}, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.01)

        # 3. Stream nội dung trả lời từ LLM
        if hasattr(response_obj, "async_response_gen"):
            # Nếu LlamaIndex hỗ trợ Async Streaming
            async for token in response_obj.async_response_gen:
                yield f"data: {json.dumps({'type': 'content', 'data': token}, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.001)
        elif hasattr(response_obj, "response_gen"):
            # Nếu là Sync Generator tiêu chuẩn
            for token in response_obj.response_gen:
                yield f"data: {json.dumps({'type': 'content', 'data': token}, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.001)
        else:
            # Nếu trả về văn bản hoàn chỉnh
            full_text = str(response_obj)
            for word in full_text.split(" "):
                yield f"data: {json.dumps({'type': 'content', 'data': word + ' '}, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.01)
                
    except Exception as e:
        # Bắt lỗi và đẩy thông báo lỗi về client dưới dạng SSE
        error_msg = f"Lỗi hệ thống RAG: {str(e)}"
        yield f"data: {json.dumps({'type': 'error', 'data': error_msg}, ensure_ascii=False)}\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        generate_rag_response(request.message), 
        media_type="text/event-stream"
    )

