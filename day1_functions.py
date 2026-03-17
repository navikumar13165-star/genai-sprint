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