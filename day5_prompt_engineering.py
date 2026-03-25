def system_prompt_demo():
    # Same question, 3 different system prompts
    question = "What is machine learning?"

    prompts = {
        "default": {
            "system": "You are a helpful assistant.",
            "expected": "General textbook answer"
        },
        "expert": {
            "system": """You are a senior ML engineer at Google.
Give technical answers with real examples.
Use precise terminology.""",
            "expected": "Deep technical answer"
        },
        "teacher": {
            "system": """You are explaining to a 10-year-old.
Use simple words and fun analogies.
Maximum 2 sentences.""",
            "expected": "Simple, short, fun answer"
        }
    }

    for name, config in prompts.items():
        print(f"\n🎭 Persona: {name}")
        print(f"   System : {config['system'][:60]}...")
        print(f"   Expects: {config['expected']}")


def few_shot_demo():
    # Show examples BEFORE asking — model learns the pattern
    prompt = """
Classify sentiment as POSITIVE, NEGATIVE, or NEUTRAL.

Example 1:
Text: "This product is amazing!"
Sentiment: POSITIVE

Example 2:
Text: "Worst experience ever."
Sentiment: NEGATIVE

Example 3:
Text: "It arrived on time."
Sentiment: NEUTRAL

Now classify:
Text: "The delivery was okay but packaging was damaged."
Sentiment:"""
    # Pattern: examples teach FORMAT + STYLE + LOGIC
    print("\n📚 Few-shot prompt built!")
    print(f"   Length: {len(prompt)} chars")
    print(f"   Examples: 3")
    return prompt


def chain_of_thought_demo():
    # WITHOUT CoT — LLM jumps to answer, often wrong
    bad_prompt = """
Q: A store has 10 apples. They sell 3, get 5 more, then sell 4.
How many apples remain?
A:"""

    # WITH CoT — LLM reasons step by step, more accurate
    good_prompt = """
Q: A store has 10 apples. They sell 3, get 5 more, then sell 4.
How many apples remain? Think step by step.

A: Let me work through this:
Step 1: Start with 10 apples
Step 2: Sell 3 → 10 - 3 = 7
Step 3: Get 5 more → 7 + 5 = 12
Step 4: Sell 4 → 12 - 4 = 8
Answer: 8 apples remain."""

    print("\n🧠 Chain-of-Thought comparison:")
    print(f"   Without CoT: {len(bad_prompt)} chars — jumps to answer")
    print(f"   With CoT   : {len(good_prompt)} chars — reasons through")
    return good_prompt


def react_pattern_demo():
    """
    ReAct = Reason + Act + Observe
    Used in LLM Agents — think, use a tool, observe result, repeat
    """
    react_prompt = """
You are an agent. For each step:
THOUGHT: reason about what to do
ACTION: call a tool [search/calculate/lookup]
OBSERVATION: what the tool returned
... repeat until you have the answer
FINAL ANSWER: your conclusion

Question: What is the GDP of Chennai's home state Tamil Nadu?

THOUGHT: I need to find Tamil Nadu's GDP.
ACTION: search("Tamil Nadu GDP 2024")
OBSERVATION: Tamil Nadu GDP is approximately ₹27 lakh crore
THOUGHT: I now have the answer.
FINAL ANSWER: Tamil Nadu's GDP is approximately ₹27 lakh crore."""

    print("\n⚛️  ReAct Pattern:")
    for line in react_prompt.split('\n'):
        if any(line.startswith(k) for k in
               ['THOUGHT', 'ACTION', 'OBSERVATION', 'FINAL']):
            print(f"   {line}")
    return react_prompt


# YOUR EXERCISE — Build a prompt builder function
def build_prompt(
    task,           # "summarise" / "classify" / "extract" / "qa"
    user_input,     # the actual content
    use_cot=False,  # add chain-of-thought instruction?
    examples=None,  # list of {"input": x, "output": y} dicts
    persona=None    # custom system persona string
):
    """
    TASK 1: Build system prompt
    - If persona given → use it
    - Else → use a default based on task type

    TASK 2: Add few-shot examples if provided
    - Format: "Input: {ex['input']}\nOutput: {ex['output']}"

    TASK 3: Add CoT instruction if use_cot=True
    - Append "Think step by step." to user_input

    TASK 4: Return dict with "system" and "user" keys
    """
    system_prompt = persona if persona else f"You are a {task} assistant."
    user_prompt = user_input
    
    if use_cot:
        user_prompt += "\nThink step by step."
    
    if examples:
        user_prompt += "\n\nFew-shot examples:"
        for ex in examples:
            user_prompt += f"\nInput: {ex['input']}\nOutput: {ex['output']}"
    
    return {"system": system_prompt, "user": user_prompt}


# Test it
result = build_prompt(
    task="classify",
    user_input="This product broke after one day.",
    use_cot=True,
    examples=[
        {"input": "Amazing quality!", "output": "POSITIVE"},
        {"input": "Total garbage.",   "output": "NEGATIVE"},
    ],
    persona="You are a sentiment analysis expert."
)

print("\n🏗️  Built Prompt:")
print(f"   System : {result['system']}")
print(f"   User   : {result['user'][:100]}...")

# Run all demos
system_prompt_demo()
few_shot_demo()
chain_of_thought_demo()
react_pattern_demo()