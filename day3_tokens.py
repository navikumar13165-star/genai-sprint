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