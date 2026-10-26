from utils import ask_ollama

INTENTS = ["Delivery Issue", "Refund Request", "Product Complaint",
           "Technical Support", "Order Cancellation", "General Inquiry"]

def detect_intent(email, subject="", model="qwen3:4b"):
    prompt = f"""Classify this customer email into exactly one category:
{", ".join(INTENTS)}
Return only the category name, with no explanation.
Subject: {subject}
Email: {email}"""
    try:
        answer = ask_ollama(prompt, model, 0)
        for intent in INTENTS:
            if intent.lower() in answer.lower():
                return intent
        return "General Inquiry"
    except Exception as e:
        return f"Intent detection failed: {e}"
