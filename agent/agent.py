# agent/agent.py

import os
import requests
from dotenv import load_dotenv

from agent.intent import classify_intent
from agent.memory import add_memory, get_memory
from agent.tools import search_verite

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are VeriBot, an AI assistant for Verité Research publications.
Persona:
- You are helpful, factual, and precise
- You ONLY answer questions related to Verité Research publications
- You politely decline unrelated questions
Rules:
- Use retrieved Verité documents when needed
- Cite the source document name and page number
- Do NOT hallucinate sources
- If unsure, say so clearly
"""

# --------------------------------------------------
# LLM CALL (SAFE, NO CRASH)
# --------------------------------------------------
def call_llm(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # REQUIRED by OpenRouter
        "HTTP-Referer": "https://huggingface.co",
        "X-Title": "VeriBot"
    }

    payload = {
        "model": "openrouter/auto",  # most stable
        "messages": messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=60
        )
        result = response.json()
    except Exception:
        return "⚠️ I’m having trouble connecting to the language model. Please try again."

    # 🔒 SAFE error handling
    if "error" in result:
        return f"⚠️ Model error: {result['error'].get('message', 'Unknown error')}"

    if "choices" not in result:
        return "⚠️ I couldn’t generate a response right now. Please try again."

    return result["choices"][0]["message"]["content"]


# --------------------------------------------------
# MAIN CHAT LOGIC (AGENTIC ROUTING)
# --------------------------------------------------
def chat(user_input: str) -> str:
    intent = classify_intent(user_input)

    # 1️⃣ Greeting → no search
    if intent == "greeting":
        return "Hello! I’m **VeriBot 🤖**, here to help you understand Verité Research publications."

    # 2️⃣ Small talk → no search
    if intent == "smalltalk":
        return "I focus on explaining Verité Research publications. Ask me anything related to them."

    # 3️⃣ Out of scope → polite refusal
    if intent == "out_of_scope":
        return "I’m only here to help with Verité Research publications."

    # 4️⃣ Verité query → vector search
    try:
        docs = search_verite(user_input)
    except Exception:
        return "⚠️ My document index is not ready yet. Please try again shortly."

    if not docs:
        return "I couldn’t find relevant information in Verité publications for that question."

    # Build context with citations
    context = ""
    for d in docs:
        source = d.metadata.get("source", "Unknown document")
        page = d.metadata.get("page", "N/A")
        context += (
            f"\n{d.page_content}\n"
            f"(Source: {source}, Page {page})\n"
        )

    # Conversation memory (string-based → SAFE)
    history = get_memory()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
Conversation history:
{history}
Retrieved context:
{context}
Question:
{user_input}
"""
        }
    ]

    answer = call_llm(messages)

    # Save memory
    add_memory(user_input, answer)

    return answer
