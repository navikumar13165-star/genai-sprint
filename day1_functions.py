def greet_user(name):
    message = "Hello " + name
    return message

# Call it anywhere
result = greet_user("Karthik")
print(result)  # "Hello Karthik"

result2 = greet_user("Priya")
print(result2)  # "Hello Priya"

def calculate_cost(price_per_token, num_tokens):
    total_cost = price_per_token * num_tokens
    return total_cost
cost = calculate_cost(0.0001, 500)
print(cost)  # 0.05

# temperature has a default — you don't HAVE to pass it

def call_llm(prompt, temperature = 0.7, max_tokens = 1024):
    print(f"Calling LLM with prompt: {prompt}")
    print(f"Temperature: {temperature}, Max Tokens: {max_tokens}")
    # In real code, the API call goes here
    return "This is a simulated LLM response"

# Call with just the required input

response = call_llm("Summarize this document.")

# Call with custom temperature

response2 = call_llm("Summarize this document.", temperature=1.2)

def build_prompt(user_question):
    prompt = "You are a helpful assistant. Answer this: " + user_question
    return prompt

def call_llm(prompt,temperature=0.7):
    # Simulating an LLM response for now
    return "This is a LLM response to: " + prompt

def answer_question(user_question):
    # Step 1: build the prompt
    prompt = build_prompt(user_question)
    # Step 2: call the LLM
    response = call_llm(prompt)
    # Step 3: return the answer
    return response

# One clean call does everything

final_answer = answer_question("What is RAG?")
print(final_answer)  # "This is a LLM response to: You are a helpful assistant. Answer this: What is RAG?"


# EXERCISE — Build a token budget checker
# Real problem: LLMs have a context window limit
# If input is too long, you need to warn the user

def check_token_budget(prompt, max_allowed_tokens):
    # Rough estimate: 1 token ≈ 4 characters
    estimated_tokens = int(len(prompt) / 4)
    
    if estimated_tokens > max_allowed_tokens:
        return f"Warning: Prompt exceeds token limit. Estimated: {estimated_tokens}, Limit: {max_allowed_tokens}"
    else:
        return f"OK:  {estimated_tokens} tokens used out of {max_allowed_tokens} allowed."

# Test it with these two calls
result1 = check_token_budget("Tell me about AI", 500)
result2 = check_token_budget("Tell me about AI " * 200, 500)  # very long prompt

print(result1)
print(result2)




# def check_token_budget(prompt, max_allowed_tokens=1024):  # ← default value!
#     estimated_tokens = int(len(prompt) / 4)
#     is_over_budget = estimated_tokens > max_allowed_tokens  # ← named boolean

#     if is_over_budget:
#         overage = estimated_tokens - max_allowed_tokens     # ← how much over?
#         return f"⚠️ Over budget by {overage} tokens! Trim your prompt."
#     else:
#         remaining = max_allowed_tokens - estimated_tokens   # ← how much left?
#         return f"✅ OK — {remaining} tokens still available."

# print(check_token_budget("Tell me about AI"))
# print(check_token_budget("Tell me about AI " * 200))