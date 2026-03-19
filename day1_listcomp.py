# OLD WAY — loop through, append one by one
scores = [0.91, 0.45, 0.87, 0.32, 0.76]

high_scores = []
for score in scores:
    high_scores.append(score)

print(high_scores)  # [0.91, 0.45, 0.87, 0.32, 0.76]

# NEW WAY — list comprehension, one clean line
high_scores = [score for score in scores]

print(high_scores)  # exact same result!

scores = [0.91, 0.45, 0.87, 0.32, 0.76]

# Only keep scores above 0.75 (relevance threshold in RAG)
relevant_scores = [score for score in scores if score > 0.75]

print(relevant_scores)  # [0.91, 0.87, 0.76]

# Convert every score to a percentage
scores = [0.91, 0.45, 0.87, 0.32, 0.76]

percentages = [round(score * 100, 1) for score in scores]

print(percentages)  # [91.0, 45.0, 87.0, 32.0, 76.0]



# USE CASE 1 — Extract just the text from a list of documents
# In RAG, retrieved docs come as objects with multiple fields
documents = [
    {"text": "Chennai is in Tamil Nadu", "score": 0.91},
    {"text": "Mumbai is in Maharashtra", "score": 0.45},
    {"text": "Bangalore is in Karnataka", "score": 0.87},
]

# Extract only the text from each document
texts = [doc["text"] for doc in documents]
print(texts)
# ['Chennai is in Tamil Nadu', 'Mumbai is in Maharashtra', 'Bangalore is in Karnataka']

# USE CASE 2 — Filter only relevant documents (score > 0.75)
relevant_docs = [doc for doc in documents if doc["score"] > 0.75]
print(relevant_docs)
# [{"text": "Chennai...", "score": 0.91}, {"text": "Bangalore...", "score": 0.87}]

# USE CASE 3 — Extract text ONLY from relevant docs (filter + transform together!)
relevant_texts = [doc["text"] for doc in documents if doc["score"] > 0.75]
print(relevant_texts)
# ['Chennai is in Tamil Nadu', 'Bangalore is in Karnataka']


# Raw responses from users are often messy
raw_inputs = ["  What is AI?  ", "TELL ME ABOUT RAG", "  langchain  "]

# Clean all of them in one line
# strip() removes spaces, lower() makes lowercase
cleaned = [text.strip().lower() for text in raw_inputs]

print(cleaned)
# ['what is ai?', 'tell me about rag', 'langchain']


# EXERCISE — RAG pipeline filter
# You just got back 5 documents from a vector database
# Your job: filter and extract only the relevant ones

search_results = [
    {"text": "LangChain is a framework for LLM apps", "score": 0.95},
    {"text": "Python was created by Guido van Rossum", "score": 0.42},
    {"text": "RAG combines retrieval with generation", "score": 0.88},
    {"text": "Chennai has a hot climate", "score": 0.31},
    {"text": "Embeddings represent text as vectors", "score": 0.79},
]

# TASK 1: Extract ALL texts (regardless of score)
all_texts = [doc["text"] for doc in search_results]

# TASK 2: Filter docs with score above 0.75
relevant_docs = [doc for doc in search_results if doc["score"] > 0.75]

# TASK 3: Extract ONLY the text from relevant docs
relevant_texts = [doc["text"] for doc in search_results if doc["score"] > 0.75]

print("All texts:", all_texts)
print("Relevant docs:", relevant_docs)
print("Relevant texts:", relevant_texts)