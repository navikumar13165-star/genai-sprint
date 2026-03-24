# The 4 main types you'll encounter in production

hallucination_types = {

    "factual_hallucination": {
        "description": "States wrong facts confidently",
        "example_prompt":   "Who invented the telephone?",
        "hallucinated":     "Thomas Edison invented the telephone in 1876.",
        "correct":          "Alexander Graham Bell invented it in 1876.",
        "danger_level":     "🔴 HIGH — users trust confident answers",
        "fix":              "RAG — ground answer in verified sources"
    },

    "source_hallucination": {
        "description": "Invents fake citations, papers, or URLs",
        "example_prompt":   "Give me a research paper on RAG",
        "hallucinated":     "'Retrieval Methods in NLP' by Smith et al., Nature 2022",
        "correct":          "No such paper exists — LLM invented it!",
        "danger_level":     "🔴 HIGH — dangerous in academic/legal contexts",
        "fix":              "Always verify citations independently"
    },

    "instruction_hallucination": {
        "description": "Ignores the actual instruction given",
        "example_prompt":   "Summarise in exactly 3 bullet points",
        "hallucinated":     "Here are 7 bullet points about the topic...",
        "correct":          "Should have given exactly 3",
        "danger_level":     "🟡 MEDIUM — breaks structured output pipelines",
        "fix":              "Lower temperature + output validation"
    },

    "context_hallucination": {
        "description": "Contradicts information in its own context",
        "example_prompt":   "Doc says price is ₹500. What is the price?",
        "hallucinated":     "The price is ₹750 based on market standards.",
        "correct":          "₹500 — as stated in the document!",
        "danger_level":     "🔴 HIGH — common in RAG without validation",
        "fix":              "Faithfulness check — answer must match context"
    },
}

print("🚨 Types of Hallucination")
print("=" * 60)
for htype, details in hallucination_types.items():
    print(f"\n📌 {htype.replace('_', ' ').title()}")
    print(f"   What     : {details['description']}")
    print(f"   Danger   : {details['danger_level']}")
    print(f"   Fix      : {details['fix']}")

def check_faithfulness(answer, context):
    """
    FAITHFULNESS CHECK:
    Does the answer contradict the context?

    In production — use an LLM to do this check.
    Here we simulate with keyword overlap.
    """
    answer_words = set(answer.lower().split())
    context_words = set(context.lower().split())

    # What % of answer words appear in context?
    overlap = answer_words.intersection(context_words)
    faithfulness_score = len(overlap) / len(answer_words) if answer_words else 0

    return round(faithfulness_score, 3)


def check_confidence_mismatch(answer):
    """
    CONFIDENCE CHECK:
    High-confidence language on uncertain topics = hallucination risk
    """
    high_confidence_phrases = [
        "definitely", "certainly", "absolutely",
        "the exact", "precisely", "always", "never",
        "100%", "guaranteed", "without doubt"
    ]

    answer_lower = answer.lower()
    flags = [p for p in high_confidence_phrases if p in answer_lower]

    return {
        "flagged_phrases": flags,
        "risk_level": "🔴 HIGH" if len(flags) >= 2
                      else "🟡 MEDIUM" if len(flags) == 1
                      else "🟢 LOW"
    }


def check_specific_claims(answer):
    """
    SPECIFICITY CHECK:
    Very specific numbers/dates without context = hallucination risk
    """
    import re

    # Look for suspiciously specific numbers
    specific_numbers = re.findall(r'\b\d{4,}\b', answer)   # 4+ digit numbers
    specific_dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b', answer)
    percentages = re.findall(r'\b\d+\.?\d*%\b', answer)

    all_specifics = specific_numbers + specific_dates + percentages
    risk = "🔴 HIGH" if len(all_specifics) > 3 else \
           "🟡 MEDIUM" if len(all_specifics) > 0 else "🟢 LOW"

    return {
        "specific_claims": all_specifics,
        "count": len(all_specifics),
        "risk_level": risk
    }


# Test all 3 checks
context = """
Our refund policy allows returns within 30 days of purchase.
Items must be unused and in original packaging.
Contact support@company.com for refund requests.
"""

good_answer = "You can return items within 30 days if they are unused."
bad_answer  = "You can definitely return items within exactly 45 days, \
100% guaranteed, and get a full refund of precisely ₹2,500."

print("\n✅ Checking GOOD answer:")
print(f"   Faithfulness : {check_faithfulness(good_answer, context)}")
print(f"   Confidence   : {check_confidence_mismatch(good_answer)['risk_level']}")
print(f"   Specificity  : {check_specific_claims(good_answer)['risk_level']}")

print("\n❌ Checking BAD answer:")
print(f"   Faithfulness : {check_faithfulness(bad_answer, context)}")
print(f"   Confidence   : {check_confidence_mismatch(bad_answer)}")
print(f"   Specificity  : {check_specific_claims(bad_answer)}")




def hallucination_reduction_guide():
    techniques = {

        "1_use_rag": {
            "technique":    "Use RAG instead of relying on LLM memory",
            "why_it_works": "Grounds answers in verified retrieved documents",
            "code_hint":    "retrieve(query, vector_store) → pass to LLM",
            "effectiveness": "⭐⭐⭐⭐⭐ Most effective"
        },

        "2_lower_temperature": {
            "technique":    "Set temperature to 0.0–0.3 for factual tasks",
            "why_it_works": "Reduces randomness — model picks safer tokens",
            "code_hint":    'config = {"temperature": 0.2}',
            "effectiveness": "⭐⭐⭐⭐ Very effective"
        },

        "3_system_prompt_instruction": {
            "technique":    "Explicitly instruct — say 'I don't know' if unsure",
            "why_it_works": "Primes the model to admit uncertainty",
            "code_hint":    '"If you don\'t know, say I don\'t have that information"',
            "effectiveness": "⭐⭐⭐ Moderately effective"
        },

        "4_output_validation": {
            "technique":    "Validate LLM output before showing to user",
            "why_it_works": "Catches obvious errors programmatically",
            "code_hint":    "check_faithfulness(answer, context) > 0.5",
            "effectiveness": "⭐⭐⭐ Moderately effective"
        },

        "5_chain_of_thought": {
            "technique":    "Ask model to reason step by step",
            "why_it_works": "Forces logical steps — errors become visible",
            "code_hint":    '"Think step by step before answering"',
            "effectiveness": "⭐⭐⭐⭐ Very effective for reasoning tasks"
        },

        "6_self_consistency": {
            "technique":    "Ask same question 3x, pick majority answer",
            "why_it_works": "Random hallucinations are inconsistent",
            "code_hint":    "responses = [call_llm(q) for _ in range(3)]",
            "effectiveness": "⭐⭐⭐ Good for critical decisions"
        },
    }

    print("\n\n🛡️  Hallucination Reduction Techniques")
    print("=" * 60)
    for key, tech in techniques.items():
        print(f"\n{key.replace('_', ' ').title()}")
        print(f"  What       : {tech['technique']}")
        print(f"  Why        : {tech['why_it_works']}")
        print(f"  Effective  : {tech['effectiveness']}")

hallucination_reduction_guide()


# EXERCISE — Hallucination Guard
# Build a complete hallucination detection pipeline
# This is used in production RAG apps!

def hallucination_guard(question, context, answer):
    """
    Run all 3 checks and return an overall risk assessment.
    If risk is HIGH — flag for human review.
    """

    # TASK 1: Run all 3 checks
    # faithfulness_score = check_faithfulness(answer, context)
    # confidence_check   = check_confidence_mismatch(answer)
    # specificity_check  = check_specific_claims(answer)
    faithfulness_score = check_faithfulness(answer, context)
    confidence_check   = check_confidence_mismatch(answer)
    specificity_check  = check_specific_claims(answer)
    # YOUR CODE

    # TASK 2: Calculate overall risk
    # HIGH if: faithfulness < 0.3 OR confidence is HIGH OR specificity is HIGH
    # MEDIUM if: faithfulness < 0.5 OR confidence is MEDIUM
    # LOW otherwise
    if faithfulness_score < 0.3 or confidence_check == "HIGH" or specificity_check == "HIGH":
        overall_risk = "HIGH"
    elif faithfulness_score < 0.5 or confidence_check == "MEDIUM":
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"
    # YOUR CODE

    # TASK 3: Return a report dict with:
    # question, answer_preview (first 50 chars),
    # faithfulness_score, overall_risk,
    # recommended_action ("✅ Safe to show" / 
    #                     "⚠️ Review before showing" / 
    #                     "🚨 Block — likely hallucination")
    report = {
        "question": question,
        "answer_preview": answer[:50],
        "faithfulness_score": faithfulness_score,
        "overall_risk": overall_risk,
        "recommended_action": "✅ Safe to show" if overall_risk == "LOW" else "⚠️ Review before showing" if overall_risk == "MEDIUM" else "🚨 Block — likely hallucination"
    }
    return report


# Test with these 3 cases
context = """
LangChain is a Python framework for building LLM applications.
It was created by Harrison Chase in 2022.
LangChain supports chains, agents, and memory modules.
Current version is 0.2.x as of 2024.
"""

tests = [
    {
        "question": "What is LangChain?",
        "answer":   "LangChain is a Python framework for building LLM apps, created by Harrison Chase."
    },
    {
        "question": "When was LangChain created?",
        "answer":   "LangChain was definitely created in 2019 with exactly 47,293 contributors worldwide."
    },
    {
        "question": "What does LangChain support?",
        "answer":   "LangChain supports chains, agents, and memory modules for LLM development."
    },
]

print("\n🔍 Hallucination Guard Results")
print("=" * 60)
for test in tests:
    report = hallucination_guard(
        test["question"],
        context,
        test["answer"]
    )
    print(f"\n❓ Q : {report['question']}")
    print(f"💬 A : {report['answer_preview']}...")
    print(f"📊 Faithfulness  : {report['faithfulness_score']}")
    print(f"⚠️  Overall Risk  : {report['overall_risk']}")
    print(f"👉 Action        : {report['recommended_action']}")