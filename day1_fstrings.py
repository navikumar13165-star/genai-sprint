# Old way — messy, error-prone
name = "Karthik"
print("Hello " + name + ", welcome to Gen AI!")

# f-string way — clean, readable
print(f"Hello {name}, welcome to Gen AI!")

model = "claude-3-sonnet"
temperature = 0.7
max_tokens = 1024

print(f"Model: {model} | Temp: {temperature} | Max Tokens: {max_tokens}")
# Model: claude-3-sonnet | Temp: 0.7 | Max Tokens: 1024

# You can do math INSIDE the curly braces
tokens_used = 350
token_limit = 1024

print(f"Tokens used: {tokens_used}")
print(f"Remaining: {token_limit - tokens_used}")        # math inside!
print(f"Usage: {round(tokens_used / token_limit * 100, 1)}%")  # percentage!


# WITHOUT f-strings — you'd have to hardcode everything
prompt = "Summarize this document in 3 bullet points in English"

# WITH f-strings — reusable for any document, language, format
def build_prompt(document_text, num_points, language):
    prompt = f"""
    You are a helpful assistant.
    Summarize the following document in {num_points} bullet points.
    Respond in {language}.

    Document:
    {document_text}
    """
    return prompt

# Now reuse it for anything!
doc = "Chennai is the capital of Tamil Nadu and a major tech hub in India."

prompt1 = build_prompt(doc, 3, "English")
prompt2 = build_prompt(doc, 5, "Tamil")

print(prompt1)
print("---")
print(prompt2)


cost = 0.000234567
similarity = 0.91823

# Limit decimal places
print(f"API cost: ${cost:.4f}")         # $0.0002  (4 decimal places)
print(f"Similarity: {similarity:.2f}")  # 0.92     (2 decimal places)
print(f"Similarity: {similarity:.0%}") # 92%      (as percentage!)

# EXERCISE — Build a RAG result formatter
# In RAG pipelines, after retrieving documents, 
# you show the user what was found before answering

def format_rag_result(question, num_docs_found, top_score, answer):
    result = f"""
    ❓ Question    : {question}
    📄 Docs Found  : {num_docs_found}
    🎯 Top Score   : {top_score:.2f}
    💬 Answer      : {answer}
    """
    return result

output = format_rag_result(
    question="What is RAG?",
    num_docs_found=4,
    top_score=0.8923,
    answer="RAG stands for Retrieval Augmented Generation."
)

print(output)