import random

def simulate_llm_response(prompt, temperature=0.7):
    """
    Simulates how temperature affects LLM responses.
    Low temp = picks the most likely word every time
    High temp = picks surprising words more often
    """
    responses = {
        "low": [
            "The capital of France is Paris.",
            "Paris is the capital of France.",
            "France's capital city is Paris.",
        ],
        "mid": [
            "Ah, Paris! The jewel of France, its beloved capital.",
            "France's capital is Paris — a city of art, love and culture.",
            "Paris, the magnificent capital of France, sits on the Seine.",
        ],
        "high": [
            "Paris! Capital! France! Baguettes! Eiffel! Oui oui!",
            "The capital... swirling... Paris... France... dancing lights!",
            "Paris is France's capital, also croissants are involved somehow.",
        ]
    }

    if temperature < 0.3:
        return random.choice(responses["low"])
    elif temperature < 1.0:
        return random.choice(responses["mid"])
    else:
        return random.choice(responses["high"])

# Test it
prompt = "What is the capital of France?"
temperatures = [0.0, 0.3, 0.7, 1.0, 1.5, 2.0]

print("=" * 60)
print(f"Prompt: '{prompt}'")
print("=" * 60)

for temp in temperatures:
    response = simulate_llm_response(prompt, temp)
    print(f"\n🌡️  Temperature: {temp}")
    print(f"💬 Response: {response}")



# These are the parameters you pass to EVERY LLM API call
# Knowing these = knowing how to control LLM behaviour

LLM_PARAMETERS = {
    # CREATIVITY CONTROL
    "temperature": {
        "range": "0.0 to 2.0",
        "default": 0.7,
        "use_cases": {
            0.0: "Factual Q&A, classification, structured output",
            0.3: "Code generation, summarisation",
            0.7: "Chatbots, general conversation",
            1.0: "Creative writing, brainstorming",
            1.5: "Poetry, experimental content",
        }
    },

    # RESPONSE LENGTH
    "max_tokens": {
        "range": "1 to model limit",
        "default": 1024,
        "use_cases": {
            50:   "One-word or one-line answers",
            256:  "Short summaries",
            1024: "Standard responses",
            4096: "Long form content, detailed analysis",
        }
    },

    # DIVERSITY CONTROL
    "top_p": {
        "range": "0.0 to 1.0",
        "default": 1.0,
        "description": "Only consider top P% of probable tokens. Lower = more focused.",
        "tip": "Use EITHER temperature OR top_p — not both!"
    },

    # REPETITION CONTROL
    "frequency_penalty": {
        "range": "-2.0 to 2.0",
        "default": 0.0,
        "description": "Positive = penalises repeating same words. Reduces repetition.",
    },

    "presence_penalty": {
        "range": "-2.0 to 2.0",
        "default": 0.0,
        "description": "Positive = encourages talking about new topics.",
    }
}

# Print a clean summary
print("\n📊 LLM Parameter Reference Card")
print("=" * 60)
for param, details in LLM_PARAMETERS.items():
    print(f"\n🔧 {param.upper()}")
    print(f"   Range   : {details.get('range', 'N/A')}")
    print(f"   Default : {details.get('default', 'N/A')}")
    if "description" in details:
        print(f"   What    : {details['description']}")



# Production settings for different Gen AI apps

PRODUCTION_CONFIGS = {
    "rag_chatbot": {
        "temperature": 0.3,    # factual, grounded in documents
        "max_tokens": 1024,
        "top_p": 0.9,
        "reason": "RAG answers must be accurate — low creativity"
    },
    "code_assistant": {
        "temperature": 0.1,    # code must be correct, not creative
        "max_tokens": 2048,
        "top_p": 0.95,
        "reason": "Code is right or wrong — minimal randomness"
    },
    "creative_writer": {
        "temperature": 1.2,    # high creativity wanted
        "max_tokens": 4096,
        "top_p": 1.0,
        "reason": "Creative writing benefits from surprising choices"
    },
    "customer_support": {
        "temperature": 0.5,    # professional but natural
        "max_tokens": 512,
        "top_p": 0.9,
        "reason": "Consistent, professional tone required"
    },
    "data_extractor": {
        "temperature": 0.0,    # always same output for same input
        "max_tokens": 256,
        "top_p": 1.0,
        "reason": "Extraction must be deterministic and reliable"
    }
}

print("\n🏭 Production Configuration Guide")
print("=" * 60)
for app, config in PRODUCTION_CONFIGS.items():
    print(f"\n📱 {app.replace('_', ' ').title()}")
    print(f"   Temperature : {config['temperature']}")
    print(f"   Max Tokens  : {config['max_tokens']}")
    print(f"   Why         : {config['reason']}")



def explain_top_p():
    """
    Temperature: scales ALL probabilities up or down
    Top_p: cuts off the BOTTOM percentage of options

    Example — next word prediction for "The sky is ___"
    Candidates: blue(60%), gray(25%), beautiful(10%), purple(4%), pizza(1%)

    Temperature=0.1 → almost always picks "blue"
    Temperature=1.5 → might pick "pizza"!

    Top_p=0.85 → only considers blue+gray (85% of probability mass)
                 never picks beautiful, purple, or pizza
    Top_p=1.0  → considers all options (default)
    """
    candidates = [
        ("blue", 0.60),
        ("gray", 0.25),
        ("beautiful", 0.10),
        ("purple", 0.04),
        ("pizza", 0.01),
    ]

    print("\n🎯 Top_p Example — 'The sky is ___'")
    print("-" * 40)
    cumulative = 0
    for word, prob in candidates:
        cumulative += prob
        included_085 = "✅" if cumulative <= 0.86 else "❌"
        included_095 = "✅" if cumulative <= 0.96 else "❌"
        bar = "█" * int(prob * 40)
        print(f"{included_085} top_p=0.85 | {included_095} top_p=0.95 | "
              f"{prob:.0%} {bar} '{word}'")

explain_top_p()



# EXERCISE — LLM Config Builder
# Build a function that recommends the right
# LLM config based on the use case

def recommend_config(use_case, expected_length="medium"):
    """
    use_case options:
        "factual_qa"      - answering facts from documents
        "code_generation" - writing code
        "creative"        - stories, poems, brainstorming
        "summarisation"   - condensing long text
        "extraction"      - pulling structured data from text

    expected_length options:
        "short"   - one line answers
        "medium"  - paragraph answers
        "long"    - detailed answers
    """

    # TASK 1: Set max_tokens based on expected_length
    # short=150, medium=512, long=2048
    if expected_length == "short":
        max_tokens = 150
    elif expected_length == "medium":
        max_tokens = 512
    elif expected_length == "long":
        max_tokens = 2048

    # TASK 2: Set temperature and top_p based on use_case
    # factual_qa   → temp=0.2, top_p=0.9
    # code_gen     → temp=0.1, top_p=0.95
    # creative     → temp=1.2, top_p=1.0
    # summarisation→ temp=0.3, top_p=0.9
    # extraction   → temp=0.0, top_p=1.0
    # unknown      → temp=0.7, top_p=1.0 (safe defaults)
    if use_case == "factual_qa":
        temperature = 0.2
        top_p = 0.9
    elif use_case == "code_generation":
        temperature = 0.1
        top_p = 0.95
    elif use_case == "creative":
        temperature = 1.2
        top_p = 1.0
    elif use_case == "summarisation":
        temperature = 0.3
        top_p = 0.9
    elif use_case == "extraction":
        temperature = 0.0
        top_p = 1.0
    else:
        temperature = 0.7
        top_p = 1.0
    # YOUR CODE

    # TASK 3: Return a config dict with:
    # temperature, max_tokens, top_p, frequency_penalty=0.3
    # and a "reasoning" string explaining your choices
    reasoning = f"For {use_case} tasks, a temperature of {temperature} " \
                f"and top_p of {top_p} helps achieve the right balance " \
                f"for {expected_length} responses."
    return {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": 0.3,
        "reasoning": reasoning
    }

    # YOUR CODE


# Test it
test_cases = [
    ("factual_qa", "medium"),
    ("code_generation", "long"),
    ("creative", "long"),
    ("extraction", "short"),
    ("unknown_task", "medium"),
]

for use_case, length in test_cases:
    config = recommend_config(use_case, length)
    print(f"\n📱 Use case : {use_case} ({length})")
    print(f"   Temp     : {config['temperature']}")
    print(f"   Tokens   : {config['max_tokens']}")
    print(f"   Top_p    : {config['top_p']}")
    print(f"   Reason   : {config['reasoning']}")