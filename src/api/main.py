import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

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

async def generate_rag_response(query: str):
    # Trả về metadata trích dẫn trước cho UI Sidebar
    sources = [
        {"file_name": "Luat_Doanh_Nghiep_2020.pdf", "page": 12, "section": "Điều 4", "text": "Doanh nghiệp là tổ chức có tên riêng, có tài sản..."},
        {"file_name": "BCTC_Vinamilk_Q2.pdf", "page": 5, "section": "KQKD", "text": "Lợi nhuận sau thuế hợp nhất đạt 2,000 tỷ đồng..."}
    ]
    yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"
    await asyncio.sleep(0.05)

    # Stream nội dung câu trả lời từng từ mượt mà
    response_text = f"Trả lời cho câu hỏi '{query}': Căn cứ theo quy định pháp luật và BCTC công bố..."
    for word in response_text.split(" "):
        yield f"data: {json.dumps({'type': 'content', 'data': word + ' '})}\n\n"
        await asyncio.sleep(0.03)

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(generate_rag_response(request.message), media_type="text/event-stream")
