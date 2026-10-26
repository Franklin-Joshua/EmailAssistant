from utils import ask_ollama

def summarize_email(email, reply="", model="qwen3:4b"):
    prompt = f"""Summarize the customer's issue and the proposed response in about 50 words.
Do not add facts. Return only the summary.
Customer email: {email}
Proposed reply: {reply}"""
    return ask_ollama(prompt, model, 0.2)
