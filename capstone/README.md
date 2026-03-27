# PDF RAG Chatbot
Upload any PDF and ask questions about it.
Powered by LLaMA 3.3 + FAISS + Streamlit.

## Setup
Enter your free Groq API key from console.groq.com
```

---

### Deploy Steps

1. Go to **huggingface.co** → Sign up free
2. Click **"New Space"**
3. Name: `pdf-rag-chatbot`
4. SDK: **Streamlit**
5. Click **"Create Space"**
6. Upload these 3 files:
   - `app.py`
   - `rag_engine.py`
   - `requirements.txt`

Your app gets a public URL:
```
https://huggingface.co/spaces/YOUR_USERNAME/pdf-rag-chatbot