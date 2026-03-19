# Loop through a list
responses = []   # ✅ your own empty list

documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

for doc in documents:
    print(f"Processing: {doc}")

# Output:
# Processing: doc1.pdf
# Processing: doc2.pdf
# Processing: doc3.pdf

# Loop exactly 5 times
for i in range(5):
    print(f"API call number: {i}")

# Output:
# API call number: 0
# API call number: 1
# API call number: 2
# API call number: 3
# API call number: 4

# range(1, 6) → starts at 1 instead of 0
for i in range(1, 6):
    print(f"Chunk {i} of 5")




chunks = [
    "Chennai is the capital of Tamil Nadu",
    "It is a major IT hub in South India",
    "Companies like Zoho and Freshworks are based here"
]

# Without enumerate — you don't know the position
for chunk in chunks:
    print(chunk)

# With enumerate — you get position + value together
for index, chunk in enumerate(chunks):
    print(f"Chunk {index}: {chunk}")

# Output:
# Chunk 0: Chennai is the capital of Tamil Nadu
# Chunk 1: It is a major IT hub in South India
# Chunk 2: Companies like Zoho and Freshworks are based here

# Keep retrying an API call until it succeeds
# (Simulated here — real API calls in Day 6)

attempts = 0
max_attempts = 3

while attempts < max_attempts:
    print(f"Attempt {attempts + 1} — calling LLM API...")
    attempts += 1

print("Done — max attempts reached")

# Output:
# Attempt 1 — calling LLM API...
# Attempt 2 — calling LLM API...
# Attempt 3 — calling LLM API...
# Done — max attempts reached


scores = [0.91, 0.45, 0.88, 0.32, 0.79]

# BREAK — stop the loop early
print("--- Finding first irrelevant doc ---")
for i, score in enumerate(scores):
    if score < 0.5:
        print(f"Irrelevant doc found at position {i} — stopping")
        break
    print(f"Doc {i} is relevant: {score}")

# CONTINUE — skip this item, move to next
print("\n--- Skipping irrelevant docs ---")
for i, score in enumerate(scores):
    if score < 0.5:
        continue   # skip low scores
    print(f"✅ Keeping doc {i}: {score}")

# Simulating what happens when you split a PDF into chunks
# and process each one

def process_chunk(chunk_text, chunk_index):
    word_count = len(chunk_text.split())
    return {
        "id": chunk_index,
        "text": chunk_text,
        "word_count": word_count
    }

raw_chunks = [
    "LangChain is a framework for building LLM applications.",
    "It supports chains, agents, and memory modules.",
    "RAG stands for Retrieval Augmented Generation.",
    "FAISS is a vector database for similarity search.",
]

# Process every chunk — this is a real RAG preprocessing step!
processed = []
for i, chunk in enumerate(raw_chunks):
    result = process_chunk(chunk, i)
    processed.append(result)
    print(f"✅ Processed chunk {i} — {result['word_count']} words")

print(f"\nTotal chunks ready: {len(processed)}")


# EXERCISE — Batch API call simulator
# In production, you often send multiple prompts 
# to an LLM and collect all responses

prompts = [
    "Summarise LangChain in one sentence",
    "What is a vector database?",
    "Explain RAG simply",
    "What is temperature in LLMs?",
    "What is a context window?"
]

def simulate_llm_call(prompt, call_number):
    # Simulating a response (real API call in Day 6!)
    return f"Response {call_number}: [Answer to '{prompt}']"

# TASK 1: Loop through all prompts using enumerate
for index, prompt in enumerate(prompts):
    # Call simulate_llm_call for each one
    response = simulate_llm_call(prompt, index + 1)
    # Store all responses in a list called 'responses'
    responses.append(response)
    # Print each response as it comes in
    print(response) 

# TASK 2: After the loop, print a summary
# "Total prompts sent: X"
# "Total responses received: X"
print(f"\nTotal prompts sent: {len(prompts)}")
print(f"Total responses received: {len(responses)}")    
# YOUR CODE HERE


import time

def batch_llm_calls(prompts, delay=0.5):
    responses = []
    failed = []

    for index, prompt in enumerate(prompts):
        try:
            response = simulate_llm_call(prompt, index + 1)
            responses.append(response)
            print(f"✅ {index + 1}/{len(prompts)} done")
            time.sleep(delay)  # avoid hitting API rate limits!
        except Exception as e:
            print(f"❌ Call {index + 1} failed: {e}")
            failed.append(index)

    print(f"\n✅ Successful: {len(responses)}")
    print(f"❌ Failed: {len(failed)}")
    return responses