import os
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"  # free, powerful!

def basic_call(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def call_with_system(system, user_message):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system",  "content": system},
            {"role": "user",    "content": user_message}
        ]
    )
    return response.choices[0].message.content

def call_with_history(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return response.choices[0].message.content

def streaming_call(prompt):
    print("🤖 ", end="", flush=True)
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        print(text, end="", flush=True)
    print()

def safe_call(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return basic_call(prompt)
        except Exception as e:
            if "rate" in str(e).lower():
                wait = 2 ** attempt
                print(f"⏳ Rate limited — waiting {wait}s...")
                time.sleep(wait)
            else:
                return f"❌ Error: {e}"
    return "❌ All retries exhausted"

def tracked_call(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    usage         = response.usage
    input_tokens  = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    # Groq is free — cost is $0!
    return {
        "response":       response.choices[0].message.content,
        "input_tokens":   input_tokens,
        "output_tokens":  output_tokens,
        "estimated_cost": "$0.00 (Groq free tier)"
    }

def build_rag_caller(system_persona, retrieved_docs, question):
    context = "\n".join([
        f"Document {i+1}: {doc}"
        for i, doc in enumerate(retrieved_docs)
    ])
    user_message = f"Context:\n{context}\n\nQuestion: {question}"
    result = tracked_call(f"{system_persona}\n\n{user_message}")
    return {
        "answer":         result["response"],
        "estimated_cost": result["estimated_cost"],
        "input_tokens":   result["input_tokens"],
        "output_tokens":  result["output_tokens"]
    }

if __name__ == "__main__":
    # Test 1 — basic
    print("=== Basic Call ===")
    print(basic_call("What is RAG in one sentence?"))

    # Test 2 — system prompt
    print("\n=== System Prompt ===")
    print(call_with_system(
        system="Answer everything like a pirate.",
        user_message="What is machine learning?"
    ))

    # Test 3 — conversation history
    print("\n=== With History ===")
    history = [
        {"role": "user",      "content": "My name is Naveenkumar"},
        {"role": "assistant", "content": "Nice to meet you Naveenkumar!"},
        {"role": "user",      "content": "What is my name?"}
    ]
    print(call_with_history(history))

    # Test 4 — streaming
    print("\n=== Streaming ===")
    streaming_call("Count from 1 to 5 slowly.")

    # Test 5 — token tracking
    print("\n=== Token Usage ===")
    result = tracked_call("Explain embeddings in 2 sentences.")
    print(f"Answer : {result['response']}")
    print(f"Tokens : {result['input_tokens']} in / {result['output_tokens']} out")
    print(f"Cost   : {result['estimated_cost']}")

    # Test 6 — YOUR RAG caller
    print("\n=== RAG Caller ===")
    docs = [
        "LangChain is a framework for LLM applications.",
        "It supports chains, agents, and memory.",
        "LangChain was created by Harrison Chase in 2022."
    ]
    result = build_rag_caller(
        system_persona="Answer only from provided documents.",
        retrieved_docs=docs,
        question="Who created LangChain?"
    )
    print(f"Answer : {result['answer']}")
    print(f"Cost   : {result['estimated_cost']}")