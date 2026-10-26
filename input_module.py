import streamlit as st

def render_email_form():
    with st.form("customer_email_form"):
        name = st.text_input("Customer name", placeholder="John")
        subject = st.text_input("Email subject", placeholder="Delivery Delay")
        email = st.text_area("Customer email", placeholder="My order has not arrived.", height=150)
        submitted = st.form_submit_button("Submit email")
    if submitted:
        if not name.strip() or not subject.strip() or not email.strip():
            st.error("Please fill in the customer name, subject, and email.")
            return None
        return {"name": name.strip(), "subject": subject.strip(), "email": email.strip()}
    return None
