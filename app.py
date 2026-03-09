import streamlit as st
from agent.agent import chat

st.title("VeriBot 🤖")
st.write("Ask about Verité Research publications")

user_input = st.text_input("Your question")

if user_input:

    response = chat(user_input)

    st.write("### Answer")
    st.write(response)