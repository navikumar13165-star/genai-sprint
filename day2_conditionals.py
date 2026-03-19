score = 0.85

if score > 0.90:
    print("Excellent match — use this document")
elif score > 0.75:
    print("Good match — usable")
elif score > 0.50:
    print("Weak match — use with caution")
else:
    print("Poor match — discard this document")

# Output: Good match — usable

# Comparison operators
score = 0.85

print(score > 0.75)    # True  — greater than
print(score < 0.75)    # False — less than
print(score == 0.85)   # True  — exactly equal (TWO equals signs!)
print(score != 0.85)   # False — not equal
print(score >= 0.85)   # True  — greater than OR equal
print(score <= 0.85)   # True  — less than OR equal

score = 0.88
word_count = 450

# AND — both must be true
if score > 0.75 and word_count < 500:
    print("✅ Document is relevant AND short enough — include it")

# OR — at least one must be true
if score > 0.90 or word_count < 100:
    print("✅ Either very relevant or very short — include it")

# NOT — flip the condition
is_empty = False
if not is_empty:
    print("✅ Document has content — process it")


documents = ["doc1.pdf", "doc2.pdf"]
config = {"model": "claude-3-sonnet", "temperature": 0.7}

# Check if something is in a list
if "doc1.pdf" in documents:
    print("doc1 is in the list")

# Check if a key exists in a dictionary
if "temperature" in config:
    print(f"Temperature is set to: {config['temperature']}")

# Check if a list is empty
retrieved_docs = []
if not retrieved_docs:
    print("⚠️ No documents retrieved — cannot answer question")


def validate_llm_response(response, min_length=10, max_length=2000):
    # Check 1 — did we get anything at all?
    if not response:
        return "❌ Empty response from LLM"

    # Check 2 — is it too short? (probably a bad response)
    if len(response) < min_length:
        return f"❌ Response too short: {len(response)} chars"

    # Check 3 — is it too long? (context window issue)
    if len(response) > max_length:
        return f"⚠️ Response too long: {len(response)} chars — consider chunking"

    # All checks passed!
    return f"✅ Valid response: {len(response)} chars"


# Test it
print(validate_llm_response(""))
print(validate_llm_response("OK"))
print(validate_llm_response("This is a great answer about RAG pipelines."))
print(validate_llm_response("word " * 500))  # very long



# EXERCISE — Smart document selector
# In a RAG pipeline, after getting search results
# you need to decide what to do based on the results

def select_documents(search_results, score_threshold=0.75):
    # search_results is a list of dicts with "text" and "score"

    # TASK 1: If search_results is empty — return a warning message
    # YOUR CODE HERE
    if not search_results:
        return "⚠️ No documents found — cannot answer question"

    # TASK 2: Filter docs above score_threshold using list comprehension
    # YOUR CODE HERE 
    # (hint: you built this in Day 1!)
    relevant_docs = [doc for doc in search_results if doc["score"] > score_threshold]

    # TASK 3: If NO docs pass the threshold — return a different warning
    # YOUR CODE HERE
    if not relevant_docs:
        return "⚠️ No relevant documents found — cannot answer question"

    # TASK 4: If 1 or 2 docs pass — return "Few results found: X docs"
    # YOUR CODE HERE
    if len(relevant_docs) <= 2:
        return f"⚠️ Few results found: {len(relevant_docs)} docs"

    # TASK 5: If more than 2 docs pass — return "Good results: X docs found"
    # YOUR CODE HERE
    return f"✅ Good results: {len(relevant_docs)} docs found"


# Test with these 3 cases
test1 = []  # empty

test2 = [   # all low scores
    {"text": "doc A", "score": 0.45},
    {"text": "doc B", "score": 0.32},
]

test3 = [   # mix of scores
    {"text": "doc A", "score": 0.91},
    {"text": "doc B", "score": 0.45},
    {"text": "doc C", "score": 0.88},
    {"text": "doc D", "score": 0.79},
]

print(select_documents(test1))
print(select_documents(test2))
print(select_documents(test3))