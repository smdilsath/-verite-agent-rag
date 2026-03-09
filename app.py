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
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="VeriBot 🤖", layout="centered")

st.title("VeriBot 🤖")
st.write("Ask about Verité Research publications")

user_input = st.text_input("Your question")

if user_input:
    response = chat(user_input)

    st.write("### Answer")
    st.write(response)