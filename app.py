import os
import streamlit as st

from rag.ingest import ingest_documents
from agent.agent import chat

# -----------------------------
# Ensure vectorstore exists
# -----------------------------
if not os.path.exists("vectorstore"):
    ingest_documents()

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="VeriBot 🤖",
    page_icon="🤖",
    layout="centered"
)

st.title("VeriBot 🤖")
st.caption("Ask questions about Verité Research publications")

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Ask a question about Verité Research…")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = chat(user_input)
            st.markdown(response)

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
