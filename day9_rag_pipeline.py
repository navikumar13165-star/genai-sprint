from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
import faiss
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
print("Key found:", bool(os.getenv("GROQ_API_KEY")))

embedder = SentenceTransformer("all-MiniLM-L6-v2")
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# ── KNOWLEDGE BASE ─────────────────────────────────
# Simulating a PDF document about Gen AI
DOCUMENT = """
LangChain is a framework for building LLM-powered applications.
It was created by Harrison Chase in October 2022.
LangChain supports Python and JavaScript.
It provides tools for chaining prompts and managing memory.

RAG stands for Retrieval Augmented Generation.
RAG combines a retriever component with a generator component.
The retriever searches a vector database for relevant chunks.
The generator is an LLM that uses retrieved chunks to answer.
RAG reduces hallucination by grounding answers in documents.

FAISS is a library developed by Facebook for similarity search.
FAISS stores embeddings as vectors and finds nearest neighbours.
Chroma is another vector database popular in LLM applications.
ChromaDB handles embedding generation automatically.

Embeddings are numerical representations of text meaning.
Similar texts have similar embeddings in vector space.
Cosine similarity measures how close two embeddings are.
The all-MiniLM-L6-v2 model generates 384-dimension embeddings.

Prompt engineering is the art of designing LLM inputs.
Few-shot prompting gives examples before asking a question.
Chain-of-thought prompting asks the model to reason step by step.
Temperature controls randomness — 0 is deterministic, 2 is chaotic.
"""


# ════════════════════════════════════════════════════
# STEP 1 — CHUNKING
# ════════════════════════════════════════════════════
def chunk_document(text, chunk_size=50, overlap=10):
    """
    TASK 1: Split text into sentences first (split by \n)
    TASK 2: Group sentences into chunks of chunk_size words
            with overlap words shared between chunks
    TASK 3: Return list of non-empty chunk strings
    """
    # YOUR CODE HERE
    sentences = [s.strip() for s in text.split("\n") if s.strip()]
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()
        if current_length + len(words) <= chunk_size:
            current_chunk.append(sentence)
            current_length += len(words)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ════════════════════════════════════════════════════
# STEP 2 — EMBED + STORE
# ════════════════════════════════════════════════════
def build_index(chunks):
    """
    TASK 4: Embed all chunks using embedder.encode()
    TASK 5: Build FAISS IndexFlatL2 index
    TASK 6: Return index + chunks + embeddings
    """
    # YOUR CODE HERE
    embeddings = embedder.encode(chunks).astype(np.float32)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks, embeddings



# ════════════════════════════════════════════════════
# STEP 3 — RETRIEVE
# ════════════════════════════════════════════════════
def retrieve(query, index, chunks, top_k=3):
    """
    TASK 7: Embed query
    TASK 8: Search FAISS index
    TASK 9: Return top_k most relevant chunks as list of strings
    """
    # YOUR CODE HERE
    query_vec = embedder.encode([query]).astype(np.float32)
    distances, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0]]



# ════════════════════════════════════════════════════
# STEP 4 — GENERATE
# ════════════════════════════════════════════════════
def generate(query, retrieved_chunks):
    """
    TASK 10: Build context string from retrieved_chunks
    TASK 11: Build RAG prompt with system + context + question
    TASK 12: Call llm.invoke() and return response text
    """
    # YOUR CODE HERE
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""You are a helpful assistant. Use the following retrieved chunks to answer the question. If the answer is not in the chunks, say you don't know.
Context:
{context}
Question: {query}
Answer:"""
    response = llm.invoke(prompt)
    return response.content.strip()



# ════════════════════════════════════════════════════
# STEP 5 — FULL PIPELINE
# ════════════════════════════════════════════════════
def rag_pipeline(query, index, chunks):
    """
    TASK 13: Call retrieve() to get relevant chunks
    TASK 14: Call generate() with query + chunks
    TASK 15: Return answer + retrieved chunks for transparency
    """
    # YOUR CODE HERE
    retrieved_chunks = retrieve(query, index, chunks)
    answer = generate(query, retrieved_chunks)
    return {"answer": answer, "chunks": retrieved_chunks}



# ── TESTS ───────────────────────────────────────────
if __name__ == "__main__":
    # Build once
    print("⏳ Building RAG pipeline...")
    chunks = chunk_document(DOCUMENT)
    index, chunks, embeddings = build_index(chunks)
    print(f"✅ {len(chunks)} chunks indexed\n")

    # Query multiple times
    questions = [
        "Who created LangChain?",
        "How does RAG reduce hallucination?",
        "What is the difference between FAISS and Chroma?",
        "What is the capital of Mars?",  # not in docs!
    ]

    for question in questions:
        print("=" * 55)
        result = rag_pipeline(question, index, chunks)
        print(f"❓ {question}")
        print(f"💬 {result['answer'][:200]}")
        print(f"📚 Sources: {len(result['chunks'])} chunks used")