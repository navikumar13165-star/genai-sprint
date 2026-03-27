# app.py — RAG PDF Chatbot UI
import streamlit as st
from rag_engine import load_pdf, chunk_text, build_index, rag_answer
import os

# ── PAGE CONFIG ────────────────────────────────────
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF RAG Chatbot")
st.caption("Upload a PDF — ask anything about it!")

# ── SIDEBAR ────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Setup")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_..."
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    # In sidebar — replace the if block
if uploaded_file and api_key:
    # Only reprocess if new file uploaded
    if "last_file" not in st.session_state or \
        st.session_state.last_file != uploaded_file.name:

        with st.spinner("📖 Reading and indexing PDF..."):
            text   = load_pdf(uploaded_file)
            chunks = chunk_text(text)
            index, embeddings = build_index(chunks)

            st.session_state.index     = index
            st.session_state.chunks    = chunks
            st.session_state.api_key   = api_key
            st.session_state.ready     = True
            st.session_state.last_file = uploaded_file.name

        st.success(f"✅ Indexed {len(chunks)} chunks!")
        st.info(f"📊 {len(text.split())} words extracted")
    else:
        st.success(f"✅ {uploaded_file.name} ready!")
elif uploaded_file and not api_key:
    st.warning("⚠️ Please enter your Groq API key to process the PDF.")

# ── CHAT ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources used"):
                for i, src in enumerate(msg["sources"]):
                    st.caption(f"Chunk {i+1}: {src[:150]}...")

# Chat input
if prompt := st.chat_input("Ask about your PDF..."):
    if not st.session_state.get("ready"):
        st.error("⚠️ Please upload a PDF and enter API key first!")
    else:
        # Show user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching PDF..."):
                answer, sources = rag_answer(
                    prompt,
                    st.session_state.index,
                    st.session_state.chunks,
                    st.session_state.api_key
                )
                st.write(answer)
                with st.expander("📚 Sources used"):
                    for i, src in enumerate(sources):
                        st.caption(f"Chunk {i+1}: {src[:150]}...")

        st.session_state.messages.append({
            "role":    "assistant",
            "content": answer,
            "sources": sources
        })