# chatbot.py — CLI Chatbot Skeleton
# Built during Day 2 of the Gen AI Sprint

import json
import time
import random

# ── Constants ──────────────────────────────────────
HISTORY_FILE = "chat_history.json"
MAX_RETRIES = 3
BOT_NAME = "GenBot"
EXIT_COMMANDS = ["exit", "quit", "bye"]

# ── Function 1: Load chat history from file ────────
def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)
            print(f"📂 Loaded {len(history)} previous messages")
            return history

    except FileNotFoundError:
        print("📂 No previous history found — starting fresh")
        return []

    except json.JSONDecodeError:
        print("⚠️ History file corrupted — starting fresh")
        return []
    
#     # TEMPORARY TEST — delete after confirming it works
# history = load_history()
# print(f"History type: {type(history)}")
# print(f"Messages loaded: {len(history)}")


# ── Function 2: Save chat history to file ──────────
def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=2)
        return True

    except Exception as e:
        print(f"⚠️ Could not save history: {e}")
        return False

# TEMPORARY TEST — delete after confirming
# test_history = []
# test_history.append({"role": "user", "content": "What is RAG?"})
# test_history.append({"role": "assistant", "content": "RAG is Retrieval Augmented Generation."})

# # Save it
# saved = save_history(test_history)
# print(f"Saved: {saved}")

# # Load it back
# loaded = load_history()
# print(f"Loaded: {len(loaded)} messages")
# print(f"First message: {loaded[0]}")

# ── Function 3: Build a prompt from history ────────
def build_prompt(history, user_input):
    # System instruction — tells LLM how to behave
    system = f"""You are {BOT_NAME}, a helpful Gen AI assistant.
Answer clearly and concisely.
If you don't know something, say so honestly."""

    # Format conversation history into readable context
    conversation = ""
    for message in history:
        role = message["role"].upper()
        content = message["content"]
        conversation += f"{role}: {content}\n"

    # Add the new user message
    conversation += f"USER: {user_input}\n"
    conversation += f"ASSISTANT: "

    # Final prompt combines system + conversation
    full_prompt = f"""
{system}

--- Conversation so far ---
{conversation}
"""
    return full_prompt

# TEMPORARY TEST — delete after confirming
# test_history = [
#     {"role": "user", "content": "What is LangChain?"},
#     {"role": "assistant", "content": "LangChain is a framework for LLM apps."},
# ]

# prompt = build_prompt(test_history, "Can you give me an example?")
# print(prompt)

# ── Function 4: Simulate an LLM API call ───────────
def simulate_llm(prompt, user_input="", attempt=1):
    
    # Simulate network delay (real APIs take 1-3 seconds)
    time.sleep(0.5)

    # Simulate random API failure (30% chance)
    if random.random() < 0.3:
        raise ConnectionError("API rate limit hit — try again")

    # Smart responses based on keywords in prompt
    prompt_lower = user_input.lower() 

    if "langchain" in prompt_lower:
        return "LangChain is a framework for building LLM-powered apps. It provides chains, agents, and memory modules."

    elif "rag" in prompt_lower:
        return "RAG stands for Retrieval Augmented Generation. It retrieves relevant documents and passes them to the LLM as context."

    elif "embedding" in prompt_lower:
        return "Embeddings are numerical representations of text. Similar texts have similar embeddings — measured using cosine similarity."

    elif "temperature" in prompt_lower:
        return "Temperature controls creativity. 0 = deterministic, 1 = creative, 2 = chaotic. Most production apps use 0.7."

    elif "vector" in prompt_lower:
        return "Vector databases like FAISS and Chroma store embeddings and allow fast similarity search across millions of documents."

    elif "agent" in prompt_lower:
        return "LLM agents use a ReAct loop — Reason, Act, Observe — to break tasks into steps and use tools to complete them."

    else:
        return f"That's a great question! As {BOT_NAME}, I'm currently in simulation mode. Real API coming on Day 6!"


def call_llm_with_retry(prompt, user_input=""):
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            response = simulate_llm(prompt, user_input, attempt + 1)
            return response

        except ConnectionError as e:
            attempt += 1
            print(f"⚠️ Attempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                print(f"⏳ Retrying in 1 second...")
                time.sleep(1)

    return "❌ Sorry — I'm having trouble connecting. Please try again."

# TEMPORARY TEST — delete after confirming
# test_history = [{"role": "user", "content": "hi"}]

# test_prompts = [
#     build_prompt(test_history, "What is RAG?"),
#     build_prompt(test_history, "Explain embeddings"),
#     build_prompt(test_history, "What is the weather?"),
# ]

# for prompt in test_prompts:
#     print("🤖 Response:", call_llm_with_retry(prompt))
#     print("---")


# ── Function 5: Main chat loop ─────────────────────
def chat_loop(history):
    print(f"\n💬 Chat started! Type any of {EXIT_COMMANDS} to quit.\n")

    while True:
        try:
            # Step 1 — Get user input
            user_input = input("You: ").strip()

            # Step 2 — Check for empty input
            if not user_input:
                print("⚠️  Please type something!\n")
                continue

            # Step 3 — Check for exit command
            if user_input.lower() in EXIT_COMMANDS:
                print(f"\n👋 {BOT_NAME}: Goodbye! Your chat has been saved.\n")
                break

            if user_input == "/history":
                if not history:
                    print("📭 No history yet!\n")
                else:
                    print("\n📜 Last 5 messages:")
                    print("-" * 30)
                # Show last 5 messages
                    recent = history[-5:] if len(history) >= 5 else history
                    for msg in recent:
                        role = "You" if msg["role"] == "user" else BOT_NAME
                        print(f"  {role}: {msg['content']}")
                    print("-" * 30 + "\n")
                    continue 
            
            if user_input == "/clear":
                confirm = input("Are you sure you want to clear the history? (yes/no): ").strip().lower()
                if confirm == "yes":
                    history = []
                    save_history(history)
                    print("✅ History cleared!\n")
                else:
                    print("⚠️ Clear cancelled.\n")
                continue 

            # Step 4 — Build the prompt with full history
            prompt = build_prompt(history, user_input)

            # Step 5 — Call the LLM
            print(f"\n{BOT_NAME}: ", end="", flush=True)
            response = call_llm_with_retry(prompt, user_input)
            print(response)
            print()

            # Step 6 — Save both messages to history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})

            # Step 7 — Persist to disk after every message
            saved = save_history(history)
            if not saved:
                print("⚠️  Warning: Could not save this message\n")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n\n👋 {BOT_NAME}: Interrupted! Saving and exiting...\n")
            save_history(history)
            break

        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Continuing chat...\n")
            continue
        

    return history


# ── Function 6: Main entry point ───────────────────
def main():
    print("=" * 50)
    print(f"  🤖 Welcome to {BOT_NAME} — Your Gen AI Assistant")
    print("=" * 50)

    # Step 1 — Load previous history
    history = load_history()

    # Step 2 — Show previous context if any
    if history:
        print(f"\n📜 Resuming from last session ({len(history)} messages)\n")
        # Show last 2 messages as context
        last_messages = history[-2:] if len(history) >= 2 else history
        for msg in last_messages:
            role = "You" if msg["role"] == "user" else BOT_NAME
            print(f"  {role}: {msg['content']}")
        print()
    
    # Step 3 — Start the chat loop
    final_history = chat_loop(history)

    # Step 4 — Final save on exit
    save_history(final_history)
    print(f"💾 Saved {len(final_history)} messages total")
    print("=" * 50)
    print("  👋 Thanks for chatting! See you next session.")
    print("=" * 50)


# ── Entry point ────────────────────────────────────
if __name__ == "__main__":
    main()


