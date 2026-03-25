from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

# ── SETUP ──────────────────────────────────────────
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# ── 1. PROMPT TEMPLATE ─────────────────────────────
# Reusable prompt — fill in variables at runtime
template = PromptTemplate(
    input_variables=["topic", "audience"],
    template="""Explain {topic} to a {audience}.
Keep it under 3 sentences."""
)

# Fill it in
prompt1 = template.format(topic="RAG", audience="5-year-old")
prompt2 = template.format(topic="RAG", audience="senior engineer")

print("=== Prompt Template ===")
print(f"Prompt 1: {prompt1}")
print(f"Prompt 2: {prompt2}")

# ── 2. LLMCHAIN ────────────────────────────────────
# Chain = PromptTemplate + LLM connected together
chain = template | llm | StrOutputParser()

print("\n=== Simple Chain ===")
result1 = chain.invoke({"topic": "embeddings", "audience": "beginner"})
result2 = chain.invoke({"topic": "embeddings", "audience": "ML engineer"})
print(f"For beginner    : {result1[:100]}...")
print(f"For ML engineer : {result2[:100]}...")

# ── 3. CONVERSATION MEMORY ─────────────────────────
# Memory stores chat history automatically
memory = InMemoryChatMessageHistory()

# Create conversation chain with memory
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

conversation = RunnableWithMessageHistory(
    chat_prompt | llm | StrOutputParser(),
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="history",
)

print("\n=== Conversation with Memory ===")

# Helper to get session history
def get_session_history(session_id: str):
    return memory

r1 = conversation.invoke(
    {"input": "My name is Naveenkumar and I am learning Gen AI"},
    config={"configurable": {"session_id": "user_1"}}
)
r2 = conversation.invoke(
    {"input": "What is my name?"},
    config={"configurable": {"session_id": "user_1"}}
)
r3 = conversation.invoke(
    {"input": "What am I learning?"},
    config={"configurable": {"session_id": "user_1"}}
)

print(f"Turn 1: {r1[:80]}...")
print(f"Turn 2: {r2[:80]}...")
print(f"Turn 3: {r3[:80]}...")

# Show what's in memory
print(f"\n📝 Memory contents:")
print(memory.messages)

# ── 4. CHAT PROMPT TEMPLATE ────────────────────────
# For chat models — system + human messages
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Gen AI tutor helping students in Chennai."),
    ("human",  "Explain {concept} in simple terms with an Indian example.")
])

chat_chain = chat_template | llm | StrOutputParser()

print("\n=== Chat Prompt Template ===")
result = chat_chain.invoke({"concept": "vector databases"})
print(result[:200])

# ── YOUR EXERCISE ───────────────────────────────────
# Build a RAG-style chain using LangChain components

def build_rag_chain(system_persona):
    """
    TASK 1: Create a ChatPromptTemplate with:
    - system: the system_persona parameter
    - human: a template that takes {context} and {question}
      Format: "Context:\n{context}\n\nQuestion: {question}"
    

    TASK 2: Create an LLMChain connecting
    your prompt template to the llm

    TASK 3: Return the chain
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_persona),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain

def run_rag_chain(chain, retrieved_docs, question):
    """
    TASK 4: Format retrieved_docs into a context string
    TASK 5: Invoke the chain with context + question
    TASK 6: Return just the answer text
    """
    context = "\n\n".join(retrieved_docs)

    result = chain.invoke({"context": context, "question": question})
    return result

# Test it
rag_chain = build_rag_chain(
    "Answer only from provided context. Say 'I don't know' if not in context."
)

docs = [
    "LangChain was created by Harrison Chase in October 2022.",
    "LangChain supports Python and JavaScript.",
    "LangChain integrates with OpenAI, Anthropic, and Groq.",
]

questions = [
    "When was LangChain created?",
    "What languages does LangChain support?",
    "Who is the CEO of Google?",   # not in docs — should say I don't know
]

print("\n=== RAG Chain ===")
for q in questions:
    answer = run_rag_chain(rag_chain, docs, q)
    print(f"\nQ: {q}")
    print(f"A: {answer[:120]}")