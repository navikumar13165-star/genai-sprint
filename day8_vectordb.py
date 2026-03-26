from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

# ── YOUR KNOWLEDGE BASE ────────────────────────────
docs = [
    "LangChain is a framework for building LLM applications.",
    "FAISS is Facebook's library for fast similarity search.",
    "RAG combines retrieval with text generation.",
    "Embeddings represent text as numerical vectors.",
    "Chennai is a major tech hub in South India.",
    "Groq provides free API access to Llama models.",
    "Chroma is a vector database built for AI applications.",
    "Transformers use attention mechanisms to process text.",
]

# ════════════════════════════════════════════════════
# PART 1 — FAISS
# ════════════════════════════════════════════════════

def build_faiss_index(documents):
    """
    TASK 1: Embed all documents using model.encode()
    TASK 2: Convert to float32 numpy array
    TASK 3: Create FAISS index with faiss.IndexFlatL2(dimension)
    TASK 4: Add embeddings to index with index.add()
    TASK 5: Return index + embeddings
    """
    # YOUR CODE HERE
    embeddings = model.encode(documents).astype(np.float32)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings


def search_faiss(query, index, documents, embeddings, top_k=3):
    """
    TASK 6: Embed the query
    TASK 7: Search index with index.search(query_vec, top_k)
    TASK 8: Return list of (score, document) tuples
    Hint: index.search returns (distances, indices)
    """
    # YOUR CODE HERE
    query_vec = model.encode([query]).astype(np.float32)
    distances, indices = index.search(query_vec, top_k)
    return [(distances[0][i], documents[indices[0][i]]) for i in range(top_k)]


# ════════════════════════════════════════════════════
# PART 2 — CHROMA
# ════════════════════════════════════════════════════

def build_chroma_collection(documents):
    """
    TASK 9:  Create chromadb client — chromadb.Client()
    TASK 10: Create collection — client.create_collection("genai_docs")
    TASK 11: Add documents with IDs
             collection.add(
                 documents=documents,
                 ids=[f"doc_{i}" for i in range(len(documents))]
             )
    TASK 12: Return collection
    """
    # YOUR CODE HERE
    client = chromadb.Client()
    collection = client.create_collection("genai_docs")
    collection.add(
        documents=documents,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )
    return collection



def search_chroma(query, collection, top_k=3):
    """
    TASK 13: Query collection —
             collection.query(query_texts=[query], n_results=top_k)
    TASK 14: Return list of (score, document) tuples
    Hint: results["distances"][0] and results["documents"][0]
    """
    # YOUR CODE HERE
    results = collection.query(query_texts=[query], n_results=top_k)
    return list(zip(results["distances"][0], results["documents"][0]))


# ── TESTS ───────────────────────────────────────────
if __name__ == "__main__":
    queries = [
        "How do I build LLM apps?",
        "What is semantic search?",
        "Tell me about Chennai",
    ]

    # FAISS
    print("=" * 50)
    print("🔵 FAISS Results")
    print("=" * 50)
    index, embeddings = build_faiss_index(docs)
    for query in queries:
        results = search_faiss(query, index, docs, embeddings)
        print(f"\n🔍 {query}")
        for score, doc in results:
            print(f"   [{score:.4f}] {doc}")

    # CHROMA
    print("\n" + "=" * 50)
    print("🟢 CHROMA Results")
    print("=" * 50)
    collection = build_chroma_collection(docs)
    for query in queries:
        results = search_chroma(query, collection)
        print(f"\n🔍 {query}")
        for score, doc in results:
            print(f"   [{score:.4f}] {doc}")