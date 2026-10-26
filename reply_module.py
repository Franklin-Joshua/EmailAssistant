from utils import ask_ollama

def generate_reply(name, subject, email, intent, similar=None, model="qwen3:4b"):
    previous = "No similar historical conversation was found."
    if similar:
        previous = f"Previous customer email: {similar['email']}\\nPrevious reply: {similar['reply']}"
    prompt = f"""You are a professional customer-support email assistant.
Write a helpful, concise, context-aware email reply. Do not invent order status,
refund approval, tracking numbers, or actions that are not confirmed. If needed,
say the support team will investigate. Address the customer naturally and end with
"Regards, Support Team".
Customer name: {name}
Subject: {subject}
Detected intent: {intent}
Customer email: {email}
Historical context (use only if relevant, do not copy blindly):
{previous}
Return only the email reply, without analysis or commentary."""
    return ask_ollama(prompt, model, 0.4)
