import streamlit as st
import requests
import json
import time

st.set_page_config(
    page_title="Trợ lý Pháp lý & Tài chính",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        padding: 1rem 0 0.5rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        font-size: 1.8rem;
        margin: 0;
    }
    .main-header p {
        color: #666;
        margin: 0.2rem 0 0 0;
        font-size: 0.9rem;
    }
    .stChatMessage {
        margin-bottom: 0.5rem;
    }
    .source-ref {
        display: inline-block;
        background: #e8f4f8;
        color: #05668d;
        border-radius: 4px;
        padding: 0 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0 2px;
        cursor: pointer;
    }
    .source-expander {
        border-left: 3px solid #05668d;
        background: #f8f9fa;
        border-radius: 4px;
        margin-bottom: 0.4rem;
        padding: 0.3rem 0.6rem;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-online {
        background: #d4edda;
        color: #155724;
    }
    .status-offline {
        background: #f8d7da;
        color: #721c24;
    }
    div[data-testid="stSidebar"] .sidebar-section {
        margin-bottom: 1rem;
    }
    div[data-testid="stSidebar"] .sidebar-section h3 {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #888;
        margin-bottom: 0.5rem;
    }
    .stAlert {
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_sources" not in st.session_state:
    st.session_state.current_sources = []
if "backend_ok" not in st.session_state:
    st.session_state.backend_ok = True
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

BACKEND_URL = "http://localhost:8000"

def check_backend():
    try:
        r = requests.get(f"{BACKEND_URL}/docs", timeout=3)
        return r.status_code == 200
    except:
        return False

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-header"><h1>⚖️📊 Trợ lý Pháp lý & Tài chính</h1><p>Tra cứu Luật Doanh nghiệp 2020 & Báo cáo tài chính — dựa trên RAG + LLM</p></div>', unsafe_allow_html=True)
with col2:
    ok = check_backend()
    st.session_state.backend_ok = ok
    badge = '<span class="status-badge status-online">● Online</span>' if ok else '<span class="status-badge status-offline">● Offline</span>'
    st.markdown(f'<div style="text-align:right;padding-top:1.2rem">{badge}</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-section"><h3>📄 Tài liệu đã index</h3></div>', unsafe_allow_html=True)
    st.caption("2 tài liệu · 212 chunks")
    st.markdown("""<div style="font-size:0.8rem;color:#666;margin-bottom:1rem">
    • <b>Luật Doanh nghiệp 2020</b> (8.4 MB)<br>
    • <b>BCTC Vinamilk Q1 2026</b> (3.7 MB)
    </div>""", unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="sidebar-section"><h3>📌 Nguồn trích dẫn</h3></div>', unsafe_allow_html=True)
    if st.session_state.current_sources:
        for idx, src in enumerate(st.session_state.current_sources, 1):
            file_name = src.get("file_name", "?")
            page = src.get("page", "?")
            text = src.get("text", "")
            section = src.get("section", "Trích đoạn")
            label = f"[{idx}] {file_name.replace('.pdf','')} — Tr.{page}"
            with st.expander(label):
                st.caption(f"**{section}**")
                st.markdown(f'<div class="source-expander">{text}</div>', unsafe_allow_html=True)
    else:
        st.info("Đặt câu hỏi để xem nguồn trích dẫn.")

    st.divider()

    st.markdown('<div class="sidebar-section"><h3>⚙️ Cấu hình</h3></div>', unsafe_allow_html=True)
    st.caption("**Model:** qwen2.5:7b (Ollama)")
    st.caption("**Embedding:** BAAI/bge-m3")
    st.caption("**Top-K:** 5 chunks")

    if st.button("🗑️ Xoá chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.current_sources = []
        st.rerun()

# --- CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if msg["role"] == "assistant" and "sources" in msg:
            content += "\n\n---\n**📚 Nguồn tham khảo:**\n" + "\n".join(
                f"- [{s.get('file_name','?')} trang {s.get('page','?')}]({s.get('section','')})"
                for s in msg["sources"][:3]
            )
        st.markdown(content)

# --- CHAT INPUT ---
disabled = not st.session_state.backend_ok
placeholder = "Hỏi về Luật Doanh nghiệp hoặc BCTC..." if st.session_state.backend_ok else "Backend chưa sẵn sàng..."
if prompt := st.chat_input(placeholder, disabled=disabled):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            res = requests.post(
                f"{BACKEND_URL}/chat/stream",
                json={"message": prompt},
                stream=True,
                timeout=(10, 300),
            )
            for line in res.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        data = json.loads(line_str[6:])
                        if data["type"] == "sources":
                            st.session_state.current_sources = data["data"]
                            st.session_state.last_sources = data["data"]
                        elif data["type"] == "content":
                            full_response += data["data"]
                            placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "sources": st.session_state.last_sources,
            })
            st.rerun()
        except requests.exceptions.Timeout:
            st.error("⏱️ Backend phản hồi quá chậm. Thử lại với câu hỏi ngắn hơn.")
        except requests.exceptions.ConnectionError:
            st.session_state.backend_ok = False
            st.error("🔌 Mất kết nối đến backend. Đảm bảo API đang chạy (`make run-api`).")
        except Exception as e:
            st.error(f"⚠️ Lỗi: {str(e)[:100]}")
