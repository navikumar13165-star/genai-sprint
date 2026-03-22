# Step 1: CHUNKING
# Why chunk? LLMs have token limits — can't feed entire PDF at once
# Each chunk = one searchable unit

def load_and_chunk(text, chunk_size=100, overlap=20):
    """
    Split text into overlapping chunks.

    chunk_size : words per chunk
    overlap    : words shared between consecutive chunks

    WHY OVERLAP? So answers at chunk boundaries aren't missed!
    Example: chunk1 ends with "refund" chunk2 starts with "within 30 days"
    Without overlap — "refund within 30 days" is split and lost!
    With overlap    — both chunks contain the full phrase ✅
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append({
            "id": len(chunks),
            "text": chunk,
            "word_count": len(chunk.split()),
            "start_word": start,
            "end_word": min(end, len(words))
        })
        # Move forward by chunk_size MINUS overlap
        start += chunk_size - overlap

    return chunks

# Test it
sample_document = """
LangChain is a framework for building LLM-powered applications.
It provides tools for chaining prompts, managing memory, and
integrating with vector databases. RAG stands for Retrieval
Augmented Generation. It combines a retriever component that
searches a knowledge base with a generator component that is
an LLM. The retriever finds relevant document chunks using
semantic similarity search. These chunks are then passed to
the LLM as context. This approach significantly reduces
hallucination because the LLM answers from retrieved facts
rather than from its training data alone. FAISS and Chroma
are popular vector databases used in RAG pipelines.
""" * 3  # repeat to make it longer

chunks = load_and_chunk(sample_document, chunk_size=30, overlap=5)

print(f"📄 Document words : {len(sample_document.split())}")
print(f"✂️  Total chunks   : {len(chunks)}")
print(f"\n📋 First 3 chunks:")
print("=" * 60)
for chunk in chunks[:3]:
    print(f"\nChunk {chunk['id']}:")
    print(f"  Words : {chunk['word_count']}")
    print(f"  Text  : {chunk['text'][:80]}...")


from sentence_transformers import SentenceTransformer
import numpy as np

def build_vector_store(chunks, model):
    """
    Embed all chunks and store them.
    This is what FAISS/Chroma does internally!
    """
    print(f"\n⏳ Embedding {len(chunks)} chunks...")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Store chunks + their embeddings together
    vector_store = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector_store.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "embedding": embedding
        })

    print(f"✅ Vector store built — {len(vector_store)} vectors")
    print(f"📐 Embedding dimensions: {len(vector_store[0]['embedding'])}")
    return vector_store


import math

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a ** 2 for a in vec1))
    mag2 = math.sqrt(sum(b ** 2 for b in vec2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)

def retrieve(query, vector_store, model, top_k=3):
    """
    Embed query → find most similar chunks.
    This is the RETRIEVER in RAG.
    """
    # Embed the query
    query_embedding = model.encode([query])[0]

    # Score every chunk
    scored = []
    for item in vector_store:
        score = cosine_similarity(
            query_embedding.tolist(),
            item["embedding"].tolist()
        )
        scored.append((score, item["text"]))

    # Return top_k most relevant
    scored.sort(reverse=True)
    return scored[:top_k]


def generate_answer(query, retrieved_chunks):
    """
    Combine retrieved chunks into a prompt.
    This is the GENERATOR in RAG.
    In production — this calls OpenAI/Anthropic API.
    Today — we simulate it.
    """
    # Build context from retrieved chunks
    context = "\n\n".join([
        f"[Source {i+1}]: {chunk}"
        for i, (score, chunk) in enumerate(retrieved_chunks)
    ])

    # Build the RAG prompt
    prompt = f"""You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't know."

Context:
{context}

Question: {query}
Answer:"""

    # Simulate answer (real LLM call in Day 6!)
    return prompt   # for now, return the prompt to see it

def rag_pipeline(query, vector_store, model, top_k=3):
    """
    The complete RAG pipeline in one function!
    """
    print(f"\n{'='*60}")
    print(f"🔍 Query: {query}")
    print(f"{'='*60}")

    # Step 4 — Retrieve
    retrieved = retrieve(query, vector_store, model, top_k)

    print(f"\n📚 Retrieved {len(retrieved)} chunks:")
    for i, (score, text) in enumerate(retrieved):
        print(f"\n  [{i+1}] Score: {score:.4f}")
        print(f"       Text : {text[:80]}...")

    # Step 5 — Generate
    prompt = generate_answer(query, retrieved)

    print(f"\n📝 Final Prompt to LLM:")
    print("-" * 60)
    print(prompt[:400] + "...")

    return prompt


# PUT IT ALL TOGETHER
model = SentenceTransformer("all-MiniLM-L6-v2")

# Offline phase — do once
chunks = load_and_chunk(sample_document, chunk_size=30, overlap=5)
vector_store = build_vector_store(chunks, model)

# Online phase — runs every query
queries = [
    "What is RAG?",
    "What vector databases are used in RAG?",
    "How does LangChain help with LLM apps?",
]

for query in queries:
    rag_pipeline(query, vector_store, model, top_k=2)



# EXERCISE — Chunking Strategy Comparison
# One of the most important RAG decisions is HOW to chunk
# Too small = loses context
# Too large = wastes token budget
# Let's compare strategies!

def chunking_report(text, strategies):
    """
    strategies = list of (chunk_size, overlap) tuples
    Compare how each strategy chunks the same document
    """
    print("📊 Chunking Strategy Comparison")
    print("=" * 60)

    for chunk_size, overlap in strategies:
        # TASK 1: Call load_and_chunk with these settings
        chunks = load_and_chunk(text, chunk_size=chunk_size, overlap=overlap)
        # YOUR CODE

        # TASK 2: Calculate average chunk word count
        avg_words = sum(chunk["word_count"] for chunk in chunks) / len(chunks) if chunks else 0
        # YOUR CODE

        # TASK 3: Print a report row showing:
        # chunk_size | overlap | num_chunks | avg_words_per_chunk
        print(f"Chunk Size: {chunk_size:4} | Overlap: {overlap:3} | "
              f"Num Chunks: {len(chunks):3} | Avg Words/Chunk: {avg_words:.1f}")
        # YOUR CODE


# Test with this document and these strategies
test_doc = """
Retrieval Augmented Generation is a technique that enhances
LLM responses by retrieving relevant information from external
knowledge bases. It works by first converting documents into
embeddings stored in vector databases. When a query arrives,
it is also embedded and used to find similar document chunks
through cosine similarity search. The top matching chunks are
then included in the LLM prompt as context. This grounds the
LLM response in factual retrieved content rather than relying
solely on parametric memory from training. RAG is particularly
useful for enterprise applications where answers must be based
on specific internal documents and policies.
""" * 5

strategies = [
    (20,  0),    # tiny chunks, no overlap
    (50,  10),   # small chunks, small overlap
    (100, 20),   # medium chunks, medium overlap
    (200, 50),   # large chunks, large overlap
    (500, 100),  # very large chunks
]

chunking_report(test_doc, strategies)