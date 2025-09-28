import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

gemini_client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Few-shot examples
FEW_SHOT_EXAMPLES = [
    {"query": "Summarize this article about AI.", "intent": "summarize"},
    {"query": "Please give me a summary of this report.", "intent": "summarize"},
    {"query": "What’s the weather in Zurich today?", "intent": "weather"},
    {"query": "Will it rain tomorrow in London?", "intent": "weather"},
    {"query": "Tell me a joke", "intent": "other"},
    {"query": "What is the capital of France?", "intent": "other"},
    {"query": "Can you give me german sentences for- Ich trinke kafee", "intent": "german_sentences"},
    {"query": "Different German Sentence for Die Wetter ist Schon", "intent": "german_sentences"},
]

async def classify_intent(query: str) -> str:
    """
    Classify the intent of the user query using few-shot examples.
    Returns: 'summarize', 'weather','german_sentences', or 'other'
    """
    system_message = (
        "You are an assistant that detects the intent of user queries. "
        "Return only one word representing the intent: 'summarize', 'weather','german_sentences', or 'other'."
    )

    # Build the few-shot message string
    few_shot_text = "Here are some examples:\n"
    for ex in FEW_SHOT_EXAMPLES:
        few_shot_text += f"Query: \"{ex['query']}\" → Intent: {ex['intent']}\n"

    user_message = f"{few_shot_text}\nClassify this query: '{query}'"

    response = gemini_client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )

    intent = response.choices[0].message.content.strip().lower()
    if intent not in ["summarize", "weather","german_sentences"]:
        intent = "other"
    return intent
