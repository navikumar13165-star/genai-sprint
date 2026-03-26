# week1_chatbot.py — Week 1 Mini Project
# LangChain + Groq + Memory + File Persistence

# week1_chatbot.py — Week 1 Mini Project
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# ── Constants ───────────────────────────────────────
HISTORY_FILE  = "week1_chat_history.json"
BOT_NAME      = "GenBot Pro"
EXIT_COMMANDS = ["exit", "quit", "bye"]
MODEL         = "llama-3.3-70b-versatile"

# ── LLM Setup ───────────────────────────────────────
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=MODEL
)

# ── Manual Memory ───────────────────────────────────
# We manage history ourselves — list of messages
chat_history = []


# ── File Persistence ────────────────────────────────
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
            # Convert saved dicts back to message objects
            messages = []
            for msg in data:
                if msg["role"] == "human":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))
            print(f"📂 Loaded {len(messages)} previous messages")
            return messages
    except FileNotFoundError:
        print("📂 Starting fresh!")
        return []

def save_history(messages):
    try:
        data = [
            {"role": "human" if isinstance(m, HumanMessage) else "ai",
             "content": m.content}
            for m in messages
        ]
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ Could not save: {e}")

    
# ── LLM Call ────────────────────────────────────────
def chat(user_input, history):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are {BOT_NAME}, a helpful Gen AI assistant.
You help students in Chennai learn AI and machine learning.
Be concise, friendly, and use simple examples."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    try:
        response = chain.invoke({
            "history": history,
            "input": user_input
        })
        return response.content

    except Exception as e:
        return f"❌ Error: {e}"
    
# ── Main Chat Loop ──────────────────────────────────
def main():
    print("=" * 50)
    print(f"  🤖 {BOT_NAME} — Powered by LangChain + Groq")
    print("=" * 50)

    # Load previous history
    history = load_history()
    if history:
        print(f"📜 Resuming — last message: {history[-1].content[:50]}...")

    print(f"\n💬 Type your question or {EXIT_COMMANDS} to quit")
    print("   Commands: /history  /clear\n")

    while True:
        try:
            user_input = input("You: ").strip()

            # Empty input
            if not user_input:
                print("⚠️  Please type something!\n")
                continue

            # Exit
            if user_input.lower() in EXIT_COMMANDS:
                save_history(history)
                print(f"\n👋 {BOT_NAME}: Goodbye! See you next session!\n")
                break

            # /history command
            if user_input == "/history":
                if not history:
                    print("📭 No history yet!\n")
                else:
                    print("\n📜 Last 4 messages:")
                    for msg in history[-4:]:
                        role = "You" if isinstance(msg, HumanMessage) else BOT_NAME
                        print(f"  {role}: {msg.content[:60]}")
                    print()
                continue

            # /clear command
            if user_input == "/clear":
                confirm = input("Clear history? (yes/no): ").strip().lower()
                if confirm == "yes":
                    history = []
                    save_history(history)
                    print("✅ History cleared!\n")
                else:
                    print("⚠️  Cancelled.\n")
                continue

            # Get LLM response
            print(f"\n{BOT_NAME}: ", end="", flush=True)
            response = chat(user_input, history)
            print(response)
            print()

            # Update memory
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response))

            # Save after every turn
            save_history(history)

        except KeyboardInterrupt:
            save_history(history)
            print(f"\n\n👋 Saved and exiting!\n")
            break

if __name__ == "__main__":
    main()