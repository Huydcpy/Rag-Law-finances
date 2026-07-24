import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG Luật & Tài chính", layout="wide", page_icon="⚖️")
st.title("⚖️📊 Trợ lý AI Tra cứu Pháp lý & Tài chính")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_sources" not in st.session_state:
    st.session_state.current_sources = []

# --- SIDEBAR TRÍCH DẪN ---
with st.sidebar:
    st.header("📄 Nguồn trích dẫn (Citations)")
    if st.session_state.current_sources:
        for idx, src in enumerate(st.session_state.current_sources, 1):
            with st.expander(f"📌 [{idx}] {src.get('file_name')} - Trang {src.get('page')}"):
                st.caption(f"**Mục/Điều:** {src.get('section')}")
                st.write(src.get('text'))
    else:
        st.info("Chưa có trích dẫn. Đặt câu hỏi để xem chi tiết căn cứ.")

# --- LỊCH SỬ CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi về Luật Doanh nghiệp hoặc BCTC..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            res = requests.post("http://localhost:8000/chat/stream", json={"message": prompt}, stream=True)
            for line in res.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        data = json.loads(line_str[6:])
                        if data["type"] == "sources":
                            st.session_state.current_sources = data["data"]
                        elif data["type"] == "content":
                            full_response += data["data"]
                            placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi kết nối Backend API: {e}")
