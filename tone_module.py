from utils import ask_ollama

def improve_tone(reply, tone, model="qwen3:4b"):
    prompt = f"""Rewrite the email below in a {tone.lower()} tone.
Preserve the meaning and all factual details. Do not add promises or invent facts.
Return only the revised email.
Email:
{reply}"""
    return ask_ollama(prompt, model, 0.4)
