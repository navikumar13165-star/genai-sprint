# Step 1 + 2 + 3 — Tokenise, Embed, Add Position

def simple_tokenise(text):
    """Split text into tokens (simplified)"""
    return text.lower().split()

def fake_embed(token, dim=4):
    """
    Real embeddings are learned during training.
    Here we simulate with hash-based values.
    """
    import hashlib
    hash_val = int(hashlib.md5(token.encode()).hexdigest(), 16)
    import random
    random.seed(hash_val)
    return [round(random.uniform(-1, 1), 3) for _ in range(dim)]

def add_positional_encoding(embeddings):
    """
    WHY? Transformers process ALL tokens simultaneously.
    Without position info — "dog bites man" = "man bites dog"!
    Position encoding adds ORDER information to each token.
    """
    import math
    positioned = []
    for pos, emb in enumerate(embeddings):
        # Add a position signal to each dimension
        pos_encoded = [
            round(val + math.sin(pos / (10000 ** (i / len(emb)))), 3)
            for i, val in enumerate(emb)
        ]
        positioned.append(pos_encoded)
    return positioned

# Test it
sentence = "RAG retrieves relevant documents"
tokens = simple_tokenise(sentence)
embeddings = [fake_embed(t) for t in tokens]
positioned = add_positional_encoding(embeddings)

print("📝 Tokenisation + Embedding + Position")
print("=" * 60)
for i, (token, emb, pos) in enumerate(zip(tokens, embeddings, positioned)):
    print(f"\nToken [{i}]: '{token}'")
    print(f"  Raw embed : {emb}")
    print(f"  + Position: {pos}")

import math

def dot_product(vec1, vec2):
    return sum(a * b for a, b in zip(vec1, vec2))

def softmax(scores):
    """
    Converts raw scores into probabilities that sum to 1.
    Highest score gets the most attention weight.
    """
    exp_scores = [math.exp(s) for s in scores]
    total = sum(exp_scores)
    return [round(e / total, 4) for e in exp_scores]

def self_attention(tokens, embeddings):
    """
    SELF-ATTENTION in simple terms:
    For each token — ask "how much should I pay
    attention to every other token?"

    Q = Query  → "What am I looking for?"
    K = Key    → "What do I contain?"
    V = Value  → "What do I give if selected?"

    Score = Q · K / sqrt(dim)
    Weight = softmax(Score)
    Output = sum(Weight × V)
    """
    dim = len(embeddings[0])
    scale = math.sqrt(dim)

    print("\n🔍 Self-Attention Scores")
    print("=" * 60)
    print("(How much each token attends to every other token)\n")

    attention_outputs = []

    for i, (token_i, query) in enumerate(zip(tokens, embeddings)):
        # Calculate attention scores with all tokens
        scores = []
        for j, (token_j, key) in enumerate(zip(tokens, embeddings)):
            score = dot_product(query, key) / scale
            scores.append(score)

        # Convert to attention weights (probabilities)
        weights = softmax(scores)

        # Print attention pattern for this token
        print(f"'{token_i}' attends to:")
        for j, (token_j, weight) in enumerate(zip(tokens, weights)):
            bar = "█" * int(weight * 30)
            print(f"  → '{token_j}': {weight:.4f} {bar}")

        # Weighted sum of values
        output = [0.0] * dim
        for weight, value in zip(weights, embeddings):
            for k in range(dim):
                output[k] += weight * value[k]

        attention_outputs.append([round(v, 3) for v in output])
        print()

    return attention_outputs

# Test it
sentence = "it chased the cat"
tokens = simple_tokenise(sentence)
embeddings = [fake_embed(t) for t in tokens]
outputs = self_attention(tokens, embeddings)

def explain_transformer_layers():
    """
    A real transformer stacks many attention layers.
    Each layer learns different patterns:
    """

    layers = {
        "Early layers (1-4)":   "Learn syntax — grammar, word order, sentence structure",
        "Middle layers (5-8)":  "Learn semantics — word meaning, entity relationships",
        "Late layers (9-12)":   "Learn task — answering, summarising, translating",
    }

    models = {
        "GPT-2 small":      {"layers": 12,  "heads": 12,  "dim": 768},
        "GPT-3":            {"layers": 96,  "heads": 96,  "dim": 12288},
        "GPT-4 (est.)":     {"layers": 120, "heads": 96,  "dim": 12288},
        "claude-3-sonnet":  {"layers": "?", "heads": "?", "dim": "?"},  # not public
        "BERT-base":        {"layers": 12,  "heads": 12,  "dim": 768},
        "all-MiniLM-L6-v2": {"layers": 6,   "heads": 12,  "dim": 384},
    }

    print("\n🏗️  Transformer Layer Functions")
    print("=" * 60)
    for layer_group, function in layers.items():
        print(f"\n{layer_group}")
        print(f"  → {function}")

    print("\n\n📊 Model Sizes")
    print("=" * 60)
    print(f"{'Model':<20} {'Layers':>8} {'Heads':>8} {'Dim':>8}")
    print("-" * 60)
    for model, specs in models.items():
        print(f"{model:<20} {str(specs['layers']):>8} "
              f"{str(specs['heads']):>8} {str(specs['dim']):>8}")

explain_transformer_layers()



def explain_architectures():
    """
    Not all transformers are the same!
    There are 3 types — know which to use when.
    """

    architectures = {

        "Encoder-only (BERT, all-MiniLM)": {
            "reads":      "Entire sequence at once — bidirectional",
            "good_for":   "Understanding, classification, embeddings",
            "example":    "Sentence embeddings, sentiment analysis",
            "analogy":    "A reader who reads the whole book before answering",
            "used_in_genai": "Embedding model in your RAG pipeline! ✅"
        },

        "Decoder-only (GPT, Claude, Llama)": {
            "reads":      "Left to right only — predicts next token",
            "good_for":   "Text generation, chatbots, completion",
            "example":    "ChatGPT, Claude, code generation",
            "analogy":    "A writer who writes one word at a time",
            "used_in_genai": "The LLM that generates your answers! ✅"
        },

        "Encoder-Decoder (T5, BART)": {
            "reads":      "Encodes input fully, decodes output step by step",
            "good_for":   "Translation, summarisation, question answering",
            "example":    "Google Translate, document summarisation",
            "analogy":    "A translator — reads all, then writes translation",
            "used_in_genai": "Specialised summarisation pipelines"
        },
    }

    print("\n\n🏛️  Transformer Architecture Types")
    print("=" * 60)
    for arch, details in architectures.items():
        print(f"\n📐 {arch}")
        for key, value in details.items():
            print(f"   {key.replace('_', ' ').title():15}: {value}")

explain_architectures()



# EXERCISE — Transformer Knowledge Checker
# Build a function that answers questions about transformers
# This simulates how you'd explain it in an interview!

def explain_concept(concept):
    """
    Return a simple explanation + real world analogy
    for each transformer concept
    """

    # TASK 1: Fill in explanation + analogy for each concept
    concepts = {

        "attention": {
            "explanation": "Focuses on relevant parts of input text",
            "analogy":     "Like reading a sentence and highlighting key words",
            "used_in":     "Every transformer layer"
        },

        "positional_encoding": {
            "explanation": "Adds position information to tokens",
            "analogy":     "Like page numbers in a book",
            "used_in":     "Input layer of transformer"
        },

        "tokenisation": {
            "explanation": "Splits text into smaller units (tokens)",
            "analogy":     "Like breaking a sentence into words",
            "used_in":     "Before text enters the model"
        },

        "softmax": {
            "explanation": "Converts raw scores into probabilities that sum to 1",
            "analogy":     "Like ranking options by preference",
            "used_in":     "Attention weight calculation"
        },

        "embedding": {
            "explanation": "Converts tokens into numerical vectors",
            "analogy":     "Like translating words into numbers",
            "used_in":     "Converting tokens to vectors"
        },
    }

    result = concepts.get(concept)
    if result:
        print(f"\n📌 {concept.upper()}")
        print(f"   What    : {result['explanation']}")
        print(f"   Analogy : {result['analogy']}")
        print(f"   Used in : {result['used_in']}")
    else:
        print(f"❌ Concept '{concept}' not found")


# Test all concepts
for concept in ["attention", "positional_encoding",
                "tokenisation", "softmax", "embedding"]:
    explain_concept(concept)