# An embedding is just a list of floating point numbers
# Each number represents a dimension of meaning

example_embedding = [0.0023, -0.0142, 0.0312, -0.0087, 0.0156]
# Real embeddings have 1536 numbers (OpenAI) or 768 (many others)

print(f"Type        : {type(example_embedding)}")
print(f"Dimensions  : {len(example_embedding)}")
print(f"First value : {example_embedding[0]}")


import math

def cosine_similarity(vec1, vec2):
    """
    Measures how similar two embeddings are.
    Returns a score between -1 and 1:
      1.0  = identical meaning
      0.0  = unrelated
     -1.0  = opposite meaning
    """
    # Dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # Magnitudes
    magnitude1 = math.sqrt(sum(a ** 2 for a in vec1))
    magnitude2 = math.sqrt(sum(b ** 2 for b in vec2))

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)

# Test with simple vectors
vec_dog    = [0.9, 0.1, 0.0, 0.8]  # simulated "dog" embedding
vec_puppy  = [0.8, 0.2, 0.0, 0.9]  # simulated "puppy" embedding
vec_cat    = [0.7, 0.1, 0.1, 0.6]  # simulated "cat" embedding
vec_democracy = [0.1, 0.9, 0.8, 0.0]  # simulated "democracy" embedding

print(f"dog vs puppy     : {cosine_similarity(vec_dog, vec_puppy):.4f}")
print(f"dog vs cat       : {cosine_similarity(vec_dog, vec_cat):.4f}")
print(f"dog vs democracy : {cosine_similarity(vec_dog, vec_democracy):.4f}")


from sentence_transformers import SentenceTransformer

# Load a small, fast embedding model
# Downloads once (~90MB), runs locally forever after
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed some sentences
sentences = [
    "What causes fever?",
    "High temperature is a symptom of infection",
    "Python is a programming language",
    "Dogs are loyal pets",
    "Machine learning uses data to learn patterns",
]

print("⏳ Generating embeddings...")
embeddings = model.encode(sentences)

print(f"✅ Done!")
print(f"Shape: {embeddings.shape}")
# Shape: (5, 384) — 5 sentences, 384 dimensions each

import numpy as np

def find_most_similar(query, documents, model):
    """
    Given a query — find the most relevant document.
    This is exactly what a vector database does!
    """
    # Embed the query
    query_embedding = model.encode([query])[0]

    # Embed all documents
    doc_embeddings = model.encode(documents)

    # Calculate similarity scores
    scores = []
    for i, doc_embedding in enumerate(doc_embeddings):
        score = cosine_similarity(
            query_embedding.tolist(),
            doc_embedding.tolist()
        )
        scores.append((score, documents[i]))

    # Sort by score — highest first
    scores.sort(reverse=True)
    return scores


# Our "knowledge base" — pretend these are PDF chunks
knowledge_base = [
    "RAG stands for Retrieval Augmented Generation.",
    "Fever is caused by infection or inflammation in the body.",
    "LangChain is a framework for building LLM applications.",
    "Python was created by Guido van Rossum in 1991.",
    "Embeddings represent text as numerical vectors.",
    "Chennai is located on the Coromandel Coast of India.",
    "FAISS is a library for efficient similarity search.",
]

# Query — note: no exact keyword match with any document!
query = "How do vector databases find relevant information?"

print(f"\n🔍 Query: '{query}'\n")
results = find_most_similar(query, knowledge_base, model)

print("📊 Results ranked by similarity:")
print("-" * 60)
for rank, (score, doc) in enumerate(results):
    bar = "█" * int(score * 20)
    print(f"{rank + 1}. [{score:.4f}] {bar}")
    print(f"   {doc}\n")


def compare_pairs(pairs, model):
    """Compare multiple pairs and show similarity scores"""
    print("\n📊 Semantic Similarity Comparison")
    print("=" * 60)

    for text1, text2 in pairs:
        emb1 = model.encode([text1])[0]
        emb2 = model.encode([text2])[0]
        score = cosine_similarity(emb1.tolist(), emb2.tolist())

        # Visual bar
        bar = "█" * int(score * 30)
        status = "✅ Similar" if score > 0.7 else "🔶 Related" if score > 0.4 else "❌ Different"

        print(f"\n{status} [{score:.4f}]")
        print(f"  A: {text1}")
        print(f"  B: {text2}")
        print(f"  {bar}")

# Test pairs
pairs = [
    ("I love dogs", "Puppies are my favourite animals"),
    ("What is machine learning?", "ML is a subset of AI"),
    ("Chennai weather is hot", "The climate in Tamil Nadu is warm"),
    ("Python programming", "Football match results"),
    ("RAG retrieves documents", "Vector search finds similar text"),
]

compare_pairs(pairs, model)


# EXERCISE — Build a mini semantic search engine
# This is a simplified version of what FAISS/Chroma does!

from sentence_transformers import SentenceTransformer
import math

model = SentenceTransformer("all-MiniLM-L6-v2")

# Your knowledge base — a mini FAQ about Gen AI
faq = [
    "LangChain is a Python framework for building LLM-powered applications.",
    "RAG combines a retriever and a generator to answer questions from documents.",
    "Temperature controls how creative or random an LLM's response is.",
    "FAISS is Facebook's library for fast similarity search on vectors.",
    "Fine-tuning trains a model on custom data to change its behaviour.",
    "Tokens are the basic units LLMs use to process and generate text.",
    "Prompt engineering is the art of designing inputs to get better LLM outputs.",
    "A context window is the maximum number of tokens an LLM can process at once.",
]

def semantic_search(query, knowledge_base, model, top_k=3):
    # TASK 1: Embed the query
    query_embedding = model.encode([query])[0]

    # TASK 2: Embed all documents in knowledge_base
    doc_embeddings = model.encode(knowledge_base)

    # TASK 3: Calculate cosine similarity between
    # query and each document
    # Store as list of (score, document) tuples
    scores = []
    for i, doc_embedding in enumerate(doc_embeddings):
        score = cosine_similarity(
            query_embedding.tolist(),
            doc_embedding.tolist()
        )
        scores.append((score, knowledge_base[i]))
    # YOUR CODE

    # TASK 4: Sort by score descending and return top_k results
    scores.sort(reverse=True)
    return scores[:top_k]
    # YOUR CODE


# Test with these queries
queries = [
    "How do I control randomness in LLM responses?",
    "What is the limit on how much text I can send to an LLM?",
    "How can I make an LLM answer questions about my own documents?",
]

for query in queries:
    print(f"\n🔍 Query: {query}")
    print("-" * 50)
    results = semantic_search(query, faq, model, top_k=2)
    for rank, (score, doc) in enumerate(results):
        print(f"  {rank + 1}. [{score:.4f}] {doc}")