def count_tokens(text):
    return len(text.split()) // 0.75  # rough estimate

def truncate_history(messages, max_tokens=500):
    """Strategy 1 — drop oldest messages until fits"""
    while messages:
        total = count_tokens(" ".join(m["content"] for m in messages))
        if total <= max_tokens:
            break
        messages.pop(0)  # drop oldest
    return messages

def sliding_window(messages, window_size=4):
    """Strategy 2 — keep only last N messages"""
    return messages[-window_size:]

def summarise_history(messages, keep_last=2):
    """Strategy 3 — compress old messages, keep recent ones"""
    if len(messages) <= keep_last:
        return messages

    old_messages = messages[:-keep_last]
    recent = messages[-keep_last:]

    # Simulate summary (real version calls LLM)
    summary_text = f"[Summary of {len(old_messages)} messages: " \
                   f"topics covered — " \
                   f"{', '.join(set(m['content'].split()[0] for m in old_messages))}]"

    summary_msg = {"role": "system", "content": summary_text}
    return [summary_msg] + recent


# Test all 3
messages = [
    {"role": "user",      "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG retrieves documents before generating answers."},
    {"role": "user",      "content": "What is LangChain?"},
    {"role": "assistant", "content": "LangChain is a framework for LLM apps."},
    {"role": "user",      "content": "What are embeddings?"},
    {"role": "assistant", "content": "Embeddings are numerical text representations."},
]

print("Original:", len(messages), "messages")
print("Truncated:", truncate_history(messages.copy(), max_tokens=50))
print("Sliding:", sliding_window(messages.copy(), window_size=4))
print("Summarised:", summarise_history(messages.copy(), keep_last=2))