# We don't have tiktoken installed yet
# so let's use the rough estimate first
import tiktoken

def estimate_tokens(text):
    """Rough estimate: 1 token ≈ 4 characters"""
    return len(text) // 4

def estimate_cost(tokens, price_per_1k=0.002):
    """OpenAI GPT-4 charges ~$0.002 per 1000 tokens"""
    return (tokens / 1000) * price_per_1k

# Test it
texts = [
    "Hello",
    "What is RAG?",
    "Explain how transformers work in simple terms",
    "You are a helpful assistant. Answer clearly." * 10,
]

print("=" * 50)
for text in texts:
    tokens = estimate_tokens(text)
    cost = estimate_cost(tokens)
    print(f"Text    : {text[:40]}...")
    print(f"Tokens  : ~{tokens}")
    print(f"Cost    : ${cost:.6f}")
    print("-" * 50)

def count_tokens_exactly(text, model="gpt-4"):
    """Count exact tokens using tiktoken"""
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    return len(tokens)

def show_tokens(text, model="gpt-4"):
    """Show how text is split into tokens"""
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    
    print(f"\nText: '{text}'")
    print(f"Token count: {len(tokens)}")
    print(f"Token IDs: {tokens}")
    
    # Decode each token to see the split
    decoded = [encoder.decode([t]) for t in tokens]
    print(f"Token split: {decoded}")

# Test it
show_tokens("Hello world")
show_tokens("Tokenization is fascinating")
show_tokens("LangChain RAG embeddings")
show_tokens("Chennai is a great city")

# Every model has a maximum token limit
CONTEXT_WINDOWS = {
    "gpt-3.5-turbo":    16_000,
    "gpt-4":            128_000,
    "claude-3-sonnet":  200_000,
    "claude-3-opus":    200_000,
    "gemini-pro":       1_000_000,
}

def check_context_window(prompt, model="gpt-4"):
    limit = CONTEXT_WINDOWS.get(model, 4096)
    used = count_tokens_exactly(prompt)
    remaining = limit - used
    percentage = round(used / limit * 100, 2)

    print(f"\n📊 Context Window Report — {model}")
    print(f"   Limit     : {limit:,} tokens")
    print(f"   Used      : {used:,} tokens ({percentage}%)")
    print(f"   Remaining : {remaining:,} tokens")

    if percentage > 90:
        print("   ⚠️  DANGER — over 90% full!")
    elif percentage > 75:
        print("   ⚠️  WARNING — getting full")
    else:
        print("   ✅  OK — plenty of space")

# Test with different sizes
short_prompt = "What is RAG?"
long_prompt = "Explain machine learning. " * 200

check_context_window(short_prompt)
check_context_window(long_prompt)

def truncate_to_token_limit(text, max_tokens=1000, model="gpt-4"):
    """
    Truncate text to fit within token limit.
    Used when documents are too long for the context window.
    """
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)

    if len(tokens) <= max_tokens:
        return text, len(tokens), False   # text, count, was_truncated

    # Truncate to max_tokens
    truncated_tokens = tokens[:max_tokens]
    truncated_text = encoder.decode(truncated_tokens)
    return truncated_text, max_tokens, True

# Test it
long_doc = "This is a very important document. " * 500

result, token_count, was_truncated = truncate_to_token_limit(long_doc, max_tokens=50)

print(f"Truncated: {was_truncated}")
print(f"Tokens   : {token_count}")
print(f"Text     : {result[:100]}...")


# EXERCISE — Token Budget Manager
# In production RAG apps, you split your token budget
# between: system prompt + retrieved docs + user question

def token_budget_manager(
    system_prompt,
    retrieved_docs,     # list of strings
    user_question,
    model="gpt-4",
    total_budget=4096
):
    # TASK 1: Count tokens for system_prompt and user_question
    system_tokens = count_tokens_exactly(system_prompt)
    question_tokens = count_tokens_exactly(user_question)

    # TASK 2: Calculate remaining budget for documents
    reserved = system_tokens + question_tokens
    doc_budget = total_budget - reserved

    # TASK 3: If doc_budget is negative — return error message
    if doc_budget < 0:
        return {
            "error": "System prompt and user question exceed total token budget.",
            "total_tokens_used": reserved,
            "docs_included": 0,
            "docs_excluded": len(retrieved_docs),
            "selected_docs": []
        }

    # TASK 4: Loop through docs, add them until budget runs out
    # Track total_doc_tokens used

    selected_docs = []
    total_doc_tokens = 0

    for doc in retrieved_docs:
        doc_tokens = count_tokens_exactly(doc)
        if total_doc_tokens + doc_tokens <= doc_budget:
            selected_docs.append(doc)
            total_doc_tokens += doc_tokens
        else:
            break   # budget exhausted

    # TASK 5: Return a summary dict with:
    # selected_docs, total_tokens_used, docs_included, docs_excluded
    return {
        "selected_docs": selected_docs,
        "total_tokens_used": reserved + total_doc_tokens,
        "docs_included": len(selected_docs),
        "docs_excluded": len(retrieved_docs) - len(selected_docs)
    }


# Test it
system = "You are a helpful assistant that answers based on provided documents."
question = "What is RAG and how does it work?"
docs = [
    "RAG stands for Retrieval Augmented Generation.",
    "It combines a retriever and a generator.",
    "The retriever finds relevant documents from a vector database.",
    "The generator is an LLM that uses those documents to answer.",
    "This reduces hallucination significantly.",
] * 50   # lots of docs to trigger budget exhaustion

result = token_budget_manager(system, docs, question)
print(f"Docs included : {result['docs_included']}")
print(f"Docs excluded : {result['docs_excluded']}")
print(f"Total tokens  : {result['total_tokens_used']}")

