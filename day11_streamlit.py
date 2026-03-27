import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("🤖 GenBot — Powered by Groq + LLaMA")
st.caption("Your Gen AI assistant")

# Session management
if "session_id" not in st.session_state:
    st.session_state.session_id = "user_001"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful Gen AI assistant.",
        height=100
    )
    if st.button("🗑️ Clear Chat"):
        requests.delete(f"{API_URL}/chat/{st.session_state.session_id}")
        st.session_state.messages = []
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Gen AI..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "message": prompt,
                        "system_prompt": system_prompt
                    }
                )
                answer = response.json()["response"]
                st.write(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                st.error(f"❌ API Error: {e}")