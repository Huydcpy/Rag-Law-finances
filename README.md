# RAG Law-Finance

Hệ thống RAG (Retrieval-Augmented Generation) cho lĩnh vực pháp luật và tài chính Việt Nam.

## Yêu cầu

- Python 3.11+
- Ollama (cho local LLM)

## Cài đặt

```bash
# Clone repo
git clone <repo-url>
cd rag-law-finance

# Cài dependencies
make install

# Copy env
cp .env.example .env

# Setup Ollama
bash scripts/setup_ollama.sh
```

## Sử dụng

```bash
# Chạy API server
make run-api

# Chạy Streamlit UI
make run-ui
```

## Cấu trúc thư mục

```
src/
├── engine/         # Core RAG pipeline
│   ├── ingestion/  # Load, parse, chunk, index
│   ├── embedding/  # Embedding models
│   ├── retrieval/  # Search strategies
│   └── generation/ # LLM + prompts
├── api/            # FastAPI routes
├── ui/             # Streamlit interface
├── configs/        # Configuration
└── utils/          # Utilities
data/
├── raw/            # Raw PDFs
├── processed/      # Parsed text
└── chroma_db/      # Vector store
```
