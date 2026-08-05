# RAG Law-Finance

Hệ thống RAG (Retrieval-Augmented Generation) cho lĩnh vực pháp luật và tài chính Việt Nam.

## Yêu cầu

- Python 3.11+
- Ollama (cho local LLM)
- poppler-utils (cho pdf2image): `sudo apt install poppler-utils`

## Cài đặt lần đầu

```bash
# 1. Clone repo
git clone <repo-url>
cd rag-law-finance

# 2. Tạo môi trường ảo và cài dependencies
python3 -m venv .venv
source .venv/bin/activate
make install

# 3. Cấu hình env (file `.env` đã có sẵn trong repo, chỉnh lại nếu cần)
#    OLLAMA_BASE_URL, LLM_MODEL_NAME, EMBEDDING_MODEL_NAME, CHROMA_PERSIST_DIR...

# 4. Pull model LLM
ollama pull qwen2.5:7b

# 5. Chạy ingestion (OCR từ PDF scan → vector store)
python3 -m src.engine.ingestion.ingest
```

## Chạy hệ thống (mỗi lần mở code)

```bash
# 1. Kích hoạt môi trường
source .venv/bin/activate

# 2. Cài dependencies (CHỈ CẦN CHẠY NẾU lỗi "No module named ..."
#    hoặc mới cài lại môi trường ảo)
pip install -e .

# 3. Khởi động Ollama (server local LLM)
ollama serve

# 4. (Terminal khác) Chạy API backend
make run-api

# 5. (Terminal khác) Chạy UI
make run-ui
```

- API: http://localhost:8000
- UI: http://localhost:8501

> **Lưu ý quan trọng:** Nếu mở web và thấy lỗi `No module named streamlit` / `uvicorn`
> nghĩa là dependencies chưa được cài vào môi trường ảo — hãy chạy lại bước 2
> (`pip install -e .`). Lần chạy đầu tiên sẽ tải model embedding `BAAI/bge-m3` (~2 GB)
> nên UI có thể chậm hơn bình thường vài phút.

## Chạy lại Ingestion (khi thêm file PDF mới vào `data/raw/`)

```bash
source .venv/bin/activate
python3 -m src.engine.ingestion.ingest
```

Lưu ý: ingestion dùng OCR nên sẽ chậm hơn so với PDF text thông thường.

## Cấu trúc thư mục

```
src/
├── engine/         # Core RAG pipeline
│   ├── ingestion/  # Load, parse (OCR), chunk, index
│   ├── embedding/  # Embedding models
│   ├── retrieval/  # Search strategies
│   └── generation/ # LLM + prompts
├── api/            # FastAPI routes
├── ui/             # Streamlit interface
├── configs/        # Configuration
└── utils/          # Utilities
data/
├── raw/            # Raw PDFs
└── chroma_db/      # Vector store (ChromaDB)
```
