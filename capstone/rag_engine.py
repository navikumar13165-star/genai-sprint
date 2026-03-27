# rag_engine.py — Core RAG logic
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
import os

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ── PDF LOADING ────────────────────────────────────
def load_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ── CHUNKING ───────────────────────────────────────
def chunk_text(text, chunk_size=200, overlap=30):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ── EMBED + INDEX ──────────────────────────────────
def build_index(chunks):
    # Guard — filter empty chunks
    chunks = [c for c in chunks if c.strip()]

    if not chunks:
        raise ValueError("No valid chunks found in PDF")

    embeddings = embedder.encode(chunks).astype(np.float32)

    # Handle 1D edge case
    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings

# ── RETRIEVE ───────────────────────────────────────
def retrieve(query, index, chunks, top_k=4):
    query_vec = embedder.encode([query]).astype(np.float32)
    distances, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0]]

# ── GENERATE ───────────────────────────────────────
def generate_answer(query, retrieved_chunks, api_key):
    client = Groq(api_key=api_key)
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""You are a helpful assistant that answers questions
based ONLY on the provided document context.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question: {query}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

# ── FULL PIPELINE ──────────────────────────────────
def rag_answer(query, index, chunks, api_key):
    retrieved = retrieve(query, index, chunks)
    answer    = generate_answer(query, retrieved, api_key)
    return answer, retrieved