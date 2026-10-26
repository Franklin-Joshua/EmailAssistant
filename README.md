# Intelligent Email Assistant — Ollama Qwen3:4b

A Streamlit app that classifies customer intent, retrieves a similar past email, generates a professional reply, rewrites tone, summarizes the issue, and saves replies.

## Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- Qwen3 4B model

## Run on Windows (PowerShell)
Open PowerShell in the `EmailAssistant` folder and run:

```powershell
ollama pull qwen3:4b
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run main.py
```

If PowerShell blocks activation, run this once for the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Ollama normally serves its API at `http://localhost:11434`. Keep Ollama running while using the app.

## Project structure
```text
EmailAssistant/
├── main.py
├── input_module.py
├── intent_module.py
├── retrieval_module.py
├── reply_module.py
├── tone_module.py
├── summary_module.py
├── utils.py
├── requirements.txt
├── data/
│   └── emails.csv
└── outputs/
    └── generated_reply.txt
```

## Notes
- Add past interactions to `data/emails.csv` with columns named `email` and `reply`.
- Similar email retrieval uses TF-IDF and cosine similarity.
- Replies are appended to `outputs/generated_reply.txt`.
- The app uses a local Ollama model; prompts and customer emails are sent to your local Ollama server, not to a hosted model API.
- Always review generated replies before sending them to a customer.
