import os
import streamlit as st
from agent.agent import chat
from rag.ingest import ingest_documents

st.title("VeriBot 🤖")
st.write("Ask about Verité Research publications")

# 🔴 CRITICAL FIX
if not os.path.exists("vectorstore"):
    ingest_documents()

user_input = st.text_input("Your question")

if user_input:
    response = chat(user_input)
    st.write("### Answer")
    st.write(response)
