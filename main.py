import streamlit as st
from input_module import render_email_form
from intent_module import detect_intent
from retrieval_module import load_emails, find_similar_email
from reply_module import generate_reply
from tone_module import improve_tone
from summary_module import summarize_email
from utils import save_reply, check_ollama

st.set_page_config(page_title="Intelligent Email Assistant", page_icon="✉️", layout="wide")
st.title("✉️ Intelligent Email Assistant")
st.caption("Powered by Ollama · Qwen3:4b")
with st.sidebar:
    st.header("Settings")
    model = st.text_input("Ollama model", "qwen3:4b")
    st.info("Make sure Ollama is running locally and the model is installed.")
    if st.button("Check Ollama connection"):
        ok, msg = check_ollama(model)
        st.success(msg) if ok else st.error(msg)

st.subheader("1. Customer email")
details = render_email_form()

if details:
    name, subject, email = details["name"], details["subject"], details["email"]
    st.markdown("#### Entered details")
    st.write(f"**Customer Name:** {name}")
    st.write(f"**Subject:** {subject}")
    st.write(f"**Customer Email:** {email}")

    if st.button("Analyze email and generate reply", type="primary", use_container_width=True):
        with st.spinner("Analyzing intent with Qwen3..."):
            intent = detect_intent(email, subject, model)
        history = load_emails()
        similar = find_similar_email(email, history)
        with st.spinner("Generating a context-aware reply..."):
            reply = generate_reply(name, subject, email, intent, similar, model)
        with st.spinner("Summarizing conversation..."):
            summary = summarize_email(email, reply, model)
        st.session_state["result"] = {
            "name": name, "subject": subject, "email": email, "intent": intent,
            "similar": similar, "reply": reply, "summary": summary, "model": model
        }

if "result" in st.session_state:
    r = st.session_state["result"]
    st.divider()
    st.subheader("2. Intent detection")
    st.success(r["intent"])
    st.subheader("3. Similar historical conversation")
    if r["similar"]:
        st.write("**Previous Email:**", r["similar"]["email"])
        st.write("**Previous Reply:**", r["similar"]["reply"])
        st.caption(f"Similarity score: {r['similar']['score']:.2f}")
    else:
        st.info("No historical emails found. Add examples to data/emails.csv.")
    st.subheader("4. AI-generated reply")
    st.text_area("Draft reply", value=r["reply"], height=220, key="reply_editor")
    st.subheader("5. Tone improver")
    tone = st.selectbox("Choose a tone", ["Friendly", "Formal", "Empathetic"])
    if st.button("Rewrite in selected tone"):
        with st.spinner("Improving tone..."):
            st.session_state["tone_reply"] = improve_tone(
                st.session_state.get("reply_editor", r["reply"]), tone, r["model"])
    if "tone_reply" in st.session_state:
        st.text_area("Improved reply", st.session_state["tone_reply"], height=220)
        if st.button("Use improved reply"):
            st.session_state["reply_editor"] = st.session_state["tone_reply"]
            st.session_state.pop("tone_reply", None)
            st.rerun()
    st.subheader("6. Conversation summary")
    st.write(r["summary"])
    st.caption("Summary is requested to be approximately 50 words.")
    st.subheader("7. Save reply")
    if st.button("Save reply to outputs/generated_reply.txt", use_container_width=True):
        saved_path = save_reply({
            "name": r["name"], "subject": r["subject"], "email": r["email"],
            "intent": r["intent"], "reply": st.session_state.get("reply_editor", r["reply"]),
            "date": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success(f"Saved to {saved_path}")
    st.download_button("Download current reply", st.session_state.get("reply_editor", r["reply"]),
                       file_name="generated_reply.txt", mime="text/plain")
