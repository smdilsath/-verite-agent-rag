import os
import requests
from dotenv import load_dotenv

from agent.tools import search_verite
from agent.memory import add_memory, get_memory
from agent.intent import detect_intent

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are VeriBot 🤖, an AI assistant for Verité Research.

Your job is to help users understand Verité publications related to:
- governance
- labour rights
- public policy
- fiscal policy

Rules:
- Use retrieved document context when answering
- Cite the document and page number
- Answer clearly and professionally
- If the question is unrelated to Verité publications, politely decline
"""

# -----------------------------
# LLM CALL
# -----------------------------
def call_llm(messages):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/auto",
        "messages": messages,
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    if "choices" not in result:
        return f"API Error: {result}"

    return result["choices"][0]["message"]["content"]


# -----------------------------
# GREETING HANDLER
# -----------------------------
def greeting_handler():

    return (
        "Hello! I'm **VeriBot 🤖**, your assistant for Verité Research publications.\n\n"
        "You can ask me questions about governance, labour rights, "
        "public policy, or other Verité research topics."
    )


# -----------------------------
# VECTOR SEARCH TOOL
# -----------------------------
def vector_search(user_input):

    docs = search_verite(user_input)

    context = ""

    for d in docs:

        text = d.page_content
        source = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "unknown")

        context += f"\n{text}\n(Source: {source}, Page {page})\n"

    return context


# -----------------------------
# MEMORY HANDLER
# -----------------------------
def memory_handler():

    history = get_memory()

    if not history:
        return ""

    formatted = ""

    for q, a in history[-3:]:   # last 3 messages only
        formatted += f"User: {q}\nAssistant: {a}\n"

    return formatted


# -----------------------------
# RESPONSE GENERATOR
# -----------------------------
def response_generator(user_input, context):

    history = memory_handler()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
Conversation History:
{history}

Context from Verité documents:
{context}

User Question:
{user_input}

Answer clearly and cite the document and page number.
"""
        }
    ]

    answer = call_llm(messages)

    return answer


# -----------------------------
# MAIN CHAT AGENT
# -----------------------------
def chat(user_input):

    intent = detect_intent(user_input)

    # Greeting
    if intent == "greeting":
        return greeting_handler()

    # Smalltalk
    elif intent == "smalltalk":
        return "I'm here to help explain Verité Research publications."

    # Follow-up (memory)
    elif intent == "followup":

        history = memory_handler()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
Conversation history:
{history}

Follow-up question:
{user_input}
"""}
        ]

        answer = call_llm(messages)

        add_memory(user_input, answer)

        return answer

    # Verité query (vector search)
    elif intent == "verite_query":

        context = vector_search(user_input)

        answer = response_generator(user_input, context)

        add_memory(user_input, answer)

        return answer

    # Out-of-scope
    else:
        return "I'm only here to help with Verité Research publications."