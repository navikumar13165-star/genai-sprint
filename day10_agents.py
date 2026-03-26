import os
import json
import math
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not set. Set it as an environment variable or in .env")
client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

# ── TOOLS ──────────────────────────────────────────
# Tools are just Python functions the LLM can call

def calculator(expression: str) -> str:
    """Evaluates a math expression"""
    try:
        # Remove spaces and validate
        expression = expression.strip()
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def search_knowledge_base(query: str) -> str:
    """Searches a mock knowledge base"""
    kb = {
        "langchain": "LangChain is a framework for LLM apps by Harrison Chase.",
        "rag": "RAG combines retrieval with generation to reduce hallucination.",
        "faiss": "FAISS is Facebook's fast similarity search library.",
        "groq": "Groq provides free API access to Llama and Mixtral models.",
        "embeddings": "Embeddings are numerical vector representations of text.",
    }
    query_lower = query.lower()
    for key, value in kb.items():
        if key in query_lower:
            return value
    return "No information found in knowledge base."

def get_word_count(text: str) -> str:
    """Counts words in text"""
    return str(len(text.split()))

# ── TOOL REGISTRY ──────────────────────────────────
TOOLS = {
    "calculator": calculator,
    "search_knowledge_base": search_knowledge_base,
    "get_word_count": get_word_count,
}

# Tool descriptions for LLM
TOOL_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression to evaluate"
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search for information about Gen AI topics",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_word_count",
            "description": "Count words in a text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to count words in"
                    }
                },
                "required": ["text"]
            }
        }
    }
]


# ── AGENT LOOP ─────────────────────────────────────
def run_agent(user_query, max_iterations=5):
    messages = [
        {"role": "system", "content": "You are a helpful agent with access to tools. Use tools when needed to answer accurately."},
        {"role": "user",   "content": user_query}
    ]

    for i in range(max_iterations):
        response = client.chat.completions.create(  # ✅ fixed
            model=MODEL,
            messages=messages,
            tools=TOOL_DESCRIPTIONS,
            tool_choice="auto"
        )

        message   = response.choices[0].message
        tool_calls = message.tool_calls

        if not tool_calls:
            return message.content

        for call in tool_calls:
            tool_name = call.function.name                    # ✅ object not dict
            tool_args = json.loads(call.function.arguments)  # ✅ parse JSON
            tool_func = TOOLS.get(tool_name)

            if tool_func:
                result = tool_func(**tool_args)
            else:
                result = f"Tool {tool_name} not found"

            print(f"\n🔄 Iteration {i+1}")
            print(f"   THOUGHT : {message.content or 'Using tool...'}")
            print(f"   ACTION  : {tool_name}({tool_args})")
            print(f"   OBSERVE : {result}")

            messages.append(message)                   # ✅ full message object
            messages.append({
                "role":         "tool",
                "tool_call_id": call.id,               # ✅ required!
                "content":      result
            })

    return "Max iterations reached"



# ── TESTS ───────────────────────────────────────────
if __name__ == "__main__":
    questions = [
        "What is 15% of 2400?",
        "What is RAG and how does it work?",
        "What is 144 divided by 12, then multiply by 7?",
    ]

    for q in questions:
        print("\n" + "=" * 55)
        print(f"❓ {q}")
        print("-" * 55)
        answer = run_agent(q)
        print(f"\n✅ Final Answer: {answer}")