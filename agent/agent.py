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
# SYSTEM PROMPT
# --------------------------------------------------
SYSTEM_PROMPT = """
You are VeriBot, an AI assistant for Verité Research publications.

Persona:
- Helpful, factual, professional
- ONLY answer questions related to Verité Research publications
- Politely decline unrelated questions

Rules:
- Use retrieved Verité documents when needed
- Cite the source document name and page number
- Do NOT hallucinate sources
- If the answer is not in the documents, say so clearly
"""

# --------------------------------------------------
# SAFE LLM CALL (NON-STREAMING → STABLE)
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

    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"

# --------------------------------------------------
# MAIN AGENT LOGIC
# --------------------------------------------------
def chat(user_input: str) -> str:
    intent = classify_intent(user_input)

    # 1️⃣ Greeting → no search
    if intent == "greeting":
        return "Hello! I’m **VeriBot 🤖**, here to help you understand Verité Research publications."

    # 2️⃣ Small talk → no search
    if intent == "smalltalk":
        return "I focus on explaining Verité Research publications. Ask me a question about them."

    # 3️⃣ Out-of-scope → polite refusal
    if intent == "out_of_scope":
        return "I’m only here to help with Verité Research publications."

    # 4️⃣ Verité question → vector search
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

    history = get_memory()

    prompt = f"""
Conversation history:
{history}

Retrieved context:
{context}

Question:
{user_input}

Answer using ONLY the context above.
Cite the source document and page number clearly.
"""

    answer = call_llm(prompt)
    add_memory(user_input, answer)

    return answer
