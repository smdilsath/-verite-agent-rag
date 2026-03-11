# agent/agent.py

import os
from dotenv import load_dotenv
from groq import Groq

from agent.intent import classify_intent
from agent.memory import add_memory, get_memory
from agent.tools import search_verite

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not set")

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"

# --------------------------------------------------
# SYSTEM PROMPT (FIXES YOUR ISSUE)
# --------------------------------------------------
SYSTEM_PROMPT = """
You are VeriBot, an AI assistant specialised in Verité Research publications.
Persona:
- Professional, factual, analytical
- Speak clearly and concisely
- Do NOT copy text verbatim unless quoting
Scope rules:
- ONLY answer questions related to Verité Research publications
- Politely refuse unrelated questions
When answering from documents:
1. FIRST explain the key finding in your own words
2. THEN support it with evidence from the documents
3. DO NOT list exhibits or tables without explanation
4. Clearly link each claim to a source and page number
5. If information is incomplete or unclear, say so explicitly
Citation rules:
- Use the document title (not file paths)
- Always include page numbers
- Tie citations directly to the statements they support
If the question is general but relevant (e.g. "What is forced labour"):
- Answer using Verité’s definition if available
- Clearly state that this is Verité Research’s interpretation
If the answer is not found in the documents:
- Say so clearly and do NOT speculate
"""

# --------------------------------------------------
# SAFE LLM CALL (STABLE, NON-STREAMING)
# --------------------------------------------------
def call_llm(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_completion_tokens=800,
            top_p=1,
        )
        return completion.choices[0].message.content.strip()

    except Exception:
        return (
            "⚠️ I’m temporarily unable to generate a response. "
            "Please try again in a moment."
        )

# --------------------------------------------------
# MAIN AGENT LOGIC (AGENTIC ROUTING)
# --------------------------------------------------
def chat(user_input: str) -> str:
    intent = classify_intent(user_input)

    # 1️⃣ Greeting → NO search
    if intent == "greeting":
        return (
            "Hello! I’m **VeriBot 🤖**, an assistant specialised in "
            "Verité Research publications."
        )

    # 2️⃣ Small talk → NO search
    if intent == "smalltalk":
        return (
            "I focus on explaining Verité Research publications. "
            "Feel free to ask a related question."
        )

    # 3️⃣ Out-of-scope → polite refusal (NO SEARCH, NO EXPLANATION)
    if intent == "out_of_scope":
        return (
        "I’m only here to help with Verité Research publications. "
        "I can’t assist with that topic."
    )

    # 4️⃣ Verité-related question → VECTOR SEARCH
    try:
        docs = search_verite(user_input)
    except Exception:
        return (
            "⚠️ My document index is not ready yet. "
            "Please try again shortly."
        )

    if not docs:
        return (
            "I couldn’t find relevant information in Verité Research "
            "publications for that question."
        )

    # --------------------------------------------------
    # BUILD CONTEXT (CLEAN & TRACEABLE)
    # --------------------------------------------------
    context = ""
    for d in docs:
        title = d.metadata.get("title", d.metadata.get("source", "Unknown document"))
        page = d.metadata.get("page", "N/A")

        context += (
            f"\n[Document: {title}, Page {page}]\n"
            f"{d.page_content}\n"
        )

    history = get_memory()

    prompt = f"""
Conversation history:
{history}
Evidence from Verité Research publications:
{context}
Question:
{user_input}
Instructions:
- Explain the answer clearly in your own words first
- Support each claim with evidence from the documents
- Cite document title and page number inline
- Do NOT list exhibits without interpretation
"""

    answer = call_llm(prompt)
    add_memory(user_input, answer)

    return answer
