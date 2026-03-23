def recommend_approach(situation):
    """
    Given a situation — recommend the right approach.
    This is the thinking process interviewers want to see!
    """

    situations = {

        # USE PROMPTING WHEN:
        "need_results_today": {
            "approach": "Prompting",
            "reason": "Zero setup time — works immediately with any LLM API",
            "example": "Customer support bot, Q&A system, summariser"
        },
        "general_knowledge_task": {
            "approach": "Prompting",
            "reason": "LLM already knows this — just guide it with instructions",
            "example": "Translation, writing assistance, code explanation"
        },
        "frequently_changing_info": {
            "approach": "RAG",
            "reason": "Fine-tuned models go stale — RAG stays current by updating the DB",
            "example": "News Q&A, product catalogue, live pricing"
        },

        # USE RAG WHEN:
        "company_specific_docs": {
            "approach": "RAG",
            "reason": "LLM doesn't know your internal docs — retrieve them at query time",
            "example": "HR policy bot, legal document Q&A, internal wiki search"
        },
        "need_source_citations": {
            "approach": "RAG",
            "reason": "RAG knows exactly which chunk it used — can cite the source",
            "example": "Research assistant, compliance checker"
        },
        "reduce_hallucination": {
            "approach": "RAG",
            "reason": "Grounding answers in retrieved facts reduces hallucination",
            "example": "Medical Q&A, financial advice, legal research"
        },

        # USE FINE-TUNING WHEN:
        "very_specific_output_format": {
            "approach": "Fine-tuning",
            "reason": "If prompting can't reliably produce exact format after many tries",
            "example": "Specific JSON structure, proprietary report format"
        },
        "specific_tone_or_style": {
            "approach": "Fine-tuning",
            "reason": "Teaching a unique brand voice that prompting can't capture",
            "example": "A company's very specific writing style across all content"
        },
        "reduce_prompt_length": {
            "approach": "Fine-tuning",
            "reason": "Fine-tuned model needs fewer instructions — saves tokens/cost at scale",
            "example": "Millions of API calls per day — every token counts"
        },
    }

    result = situations.get(situation, {
        "approach": "Prompting",
        "reason": "Default to prompting first — it's fastest and cheapest",
        "example": "Always start here before considering other approaches"
    })

    return result

# Test it
test_situations = [
    "company_specific_docs",
    "need_results_today",
    "very_specific_output_format",
    "reduce_hallucination",
    "frequently_changing_info",
]

print("🎯 Approach Recommender")
print("=" * 60)
for situation in test_situations:
    result = recommend_approach(situation)
    print(f"\n📌 Situation : {situation.replace('_', ' ').title()}")
    print(f"   Approach  : {result['approach']}")
    print(f"   Reason    : {result['reason']}")
    print(f"   Example   : {result['example']}")


def compare_costs():
    approaches = {
        "Prompting": {
            "setup_time":     "0 days",
            "setup_cost":     "$0",
            "per_query_cost": "High (long prompts = more tokens)",
            "maintenance":    "Low — update the prompt string",
            "scalability":    "Excellent — just call the API",
            "when_expensive": "When you have millions of queries/day",
        },
        "RAG": {
            "setup_time":     "1–3 days",
            "setup_cost":     "$10–$100 (vector DB + embedding costs)",
            "per_query_cost": "Medium (retrieval + LLM call)",
            "maintenance":    "Medium — keep vector DB updated",
            "scalability":    "Good — vector search is fast",
            "when_expensive": "When documents change very frequently",
        },
        "Fine-tuning": {
            "setup_time":     "1–4 weeks",
            "setup_cost":     "$100–$10,000+ (training compute)",
            "per_query_cost": "Low (shorter prompts needed)",
            "maintenance":    "High — retrain when base model updates",
            "scalability":    "Excellent once trained",
            "when_expensive": "Almost always — avoid unless necessary!",
        },
    }

    print("\n💰 Cost & Effort Comparison")
    print("=" * 60)
    for approach, details in approaches.items():
        print(f"\n🔧 {approach.upper()}")
        for key, value in details.items():
            print(f"   {key.replace('_', ' ').title():20}: {value}")

compare_costs()


def decision_tree(requirements):
    """
    Walk through the exact decision process interviewers want.
    requirements = dict of booleans
    """

    print("\n🌳 RAG vs Fine-tuning vs Prompting — Decision Tree")
    print("=" * 60)

    # Question 1
    if requirements.get("needs_custom_knowledge"):
        print("✅ Needs custom/private knowledge → eliminate vanilla prompting")

        # Question 2
        if requirements.get("data_changes_frequently"):
            print("✅ Data changes frequently → RAG wins (update DB, not model)")
            return "RAG"

        elif requirements.get("needs_exact_output_format"):
            print("✅ Needs very specific output format → Fine-tuning wins")
            return "Fine-tuning"

        else:
            print("✅ Static knowledge, flexible format → RAG wins")
            return "RAG"

    # Question 3
    elif requirements.get("needs_specific_style"):
        if requirements.get("high_query_volume"):
            print("✅ High volume + specific style → Fine-tuning (saves tokens)")
            return "Fine-tuning"
        else:
            print("✅ Specific style, low volume → Prompting (system prompt)")
            return "Prompting"

    else:
        print("✅ General task → Prompting (fastest, cheapest)")
        return "Prompting"


# Test different scenarios
scenarios = [
    {
        "name": "Internal HR chatbot",
        "needs_custom_knowledge": True,
        "data_changes_frequently": True,
        "needs_exact_output_format": False,
        "needs_specific_style": False,
        "high_query_volume": False,
    },
    {
        "name": "Legal document analyser",
        "needs_custom_knowledge": True,
        "data_changes_frequently": False,
        "needs_exact_output_format": False,
        "needs_specific_style": False,
        "high_query_volume": False,
    },
    {
        "name": "Brand content generator",
        "needs_custom_knowledge": False,
        "data_changes_frequently": False,
        "needs_exact_output_format": False,
        "needs_specific_style": True,
        "high_query_volume": True,
    },
    {
        "name": "General Q&A assistant",
        "needs_custom_knowledge": False,
        "data_changes_frequently": False,
        "needs_exact_output_format": False,
        "needs_specific_style": False,
        "high_query_volume": False,
    },
]

for scenario in scenarios:
    name = scenario.pop("name")
    print(f"\n📌 Scenario: {name}")
    recommendation = decision_tree(scenario)
    print(f"🎯 Recommendation: {recommendation}")
    print("-" * 60)


# EXERCISE — The Interview Simulator
# Answer these 3 scenarios like an interviewer would ask
# Build a function that explains the reasoning clearly

def interview_answer(scenario):
    """
    Given a scenario — return a structured interview answer
    with: recommendation, top_reason, tradeoff, example
    """

    # SCENARIO 1: "We have 10,000 customer support PDFs
    # and want to answer customer questions accurately"
    if scenario == "customer_support_pdfs":
        return {
            "recommendation": "RAG",
            "top_reason":     "RAG is ideal for handling large volumes of custom knowledge and frequent data updates.",
            "tradeoff":       "RAG requires more infrastructure and maintenance compared to prompting.",
            "example_stack":  "LangChain + FAISS + OpenAI"
        }

    # SCENARIO 2: "We want our LLM to always respond
    # in our brand's exact tone and JSON format"
    elif scenario == "brand_tone_json":
        return {
            "recommendation": "Fine-tuning",
            "top_reason":     "Fine-tuning allows for precise control over output format and style.",
            "tradeoff":       "Fine-tuning requires more computational resources and time to train.",
            "example_stack":  "Hugging Face Transformers + Custom Training Script"
        }

    # SCENARIO 3: "We need to summarise news articles
    # in 3 bullet points — 10,000 articles per day"
    elif scenario == "news_summariser":        
        return {
        "recommendation": "Prompting",
        "top_reason":     "Articles are passed directly — no retrieval needed. Simple system prompt handles the format.",
        "tradeoff":       "At 10K articles/day token costs add up — fine-tuning could reduce cost at massive scale.",
        "example_stack":  "OpenAI API + Python — no vector DB needed!"
    }

    # SCENARIO 3: "We need to summarise news articles
    # in 3 bullet points — 10,000 articles per day"
    elif scenario == "news_summariser":
        return {
            "recommendation": "RAG",
            "top_reason":     "RAG can handle large volumes of frequently changing information by updating the vector database.",
            "tradeoff":       "RAG has higher setup and maintenance costs than prompting.",
            "example_stack":  "LangChain + FAISS + OpenAI"
        }

# Test it
for scenario in ["customer_support_pdfs", "brand_tone_json", "news_summariser"]:
    print(f"\n📌 Scenario: {scenario}")
    answer = interview_answer(scenario)
    for key, value in answer.items():
        print(f"   {key:20}: {value}")