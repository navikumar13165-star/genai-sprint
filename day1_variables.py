# 1. String — for text, prompts, responses
model_name = "gpt-4"
user_prompt = "Summarize this document in 3 bullet points"

# 2. Integer — for whole numbers
max_tokens = 1024
num_chunks = 5

# 3. Float — for decimal numbers
temperature = 0.7      # controls how creative the LLM is
similarity_score = 0.91  # how similar two embeddings are

# 4. Boolean — True or False only
is_streaming = True
use_memory = False

# 5. None — means "nothing" / "not set yet"
api_response = None    # before the API call is made


# LIST — ordered collection, can change it
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
scores = [0.91, 0.85, 0.76]

# Access items by position (starts at 0)
print(documents[0])   # "doc1.pdf"
print(scores[-1])     # 0.76  ← -1 always means last item

# DICTIONARY — key:value pairs (like a form)
llm_config = {
    "model": "claude-3-sonnet",
    "temperature": 0.7,
    "max_tokens": 1024
}

# Access by key
print(llm_config["model"])        # "claude-3-sonnet"
print(llm_config["temperature"])  # 0.7



print(type(model_name))    # <class 'str'>
print(type(max_tokens))    # <class 'int'>
print(type(temperature))   # <class 'float'>
print(type(is_streaming))  # <class 'bool'>
print(type(documents))     # <class 'list'>
print(type(llm_config))    # <class 'dict'>

print(type(model_name))    # <class 'str'>
print(type(max_tokens))    # <class 'int'>
print(type(temperature))   # <class 'float'>
print(type(is_streaming))  # <class 'bool'>
print(type(documents))     # <class 'list'>
print(type(llm_config))    # <class 'dict'>

# Start with no response
api_response = None
print(api_response)   # None

# Simulate receiving a response from an LLM
api_response = "The document talks about climate change in South India."
print(api_response)   # The document talks about...

# Update token count
total_tokens = 0
total_tokens = total_tokens + 150   # after first call
total_tokens = total_tokens + 230   # after second call
print(total_tokens)   # 380

# Shorthand (same thing)
total_tokens += 300
print(total_tokens)   # 680


# YOUR EXERCISE — fill in the blanks
# Build a config for a RAG chatbot

chatbot_name = "Chennai PDF Bot"
llm_model = "gpt-4"
chunk_size = 500
is_active = True
retrieved_docs = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

# Print all of them
print(chatbot_name)
print(llm_model)
print(chunk_size)
print(is_active)
print(retrieved_docs)
print(retrieved_docs[1])  # print just the second document