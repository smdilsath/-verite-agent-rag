# agent/intent.py

import re

def classify_intent(user_input: str) -> str:
    text = user_input.lower().strip()

    # 1️⃣ Greetings
    if re.match(r"^(hi|hello|hey|good morning|good evening)\b", text):
        return "greeting"

    # 2️⃣ Small talk
    if text in {"how are you", "how are you?", "what can you do", "what can you do?"}:
        return "smalltalk"

    # 3️⃣ Explicit out-of-scope (people, sports, entertainment, general knowledge)
    out_of_scope_keywords = [
        "who is", "who's", "virat", "kohli", "messi", "cricket",
        "football", "actor", "movie", "song", "president of",
        "capital of", "weather", "google", "chatgpt"
    ]

    if any(k in text for k in out_of_scope_keywords):
        return "out_of_scope"

    # 4️⃣ Verité-related keywords
    verite_keywords = [
        "verité", "verite",
        "rti", "right to information",
        "beneficial ownership",
        "forced labour",
        "public authority",
        "proactive disclosure",
        "imf", "fatf"
    ]

    if any(k in text for k in verite_keywords):
        return "verite_query"

    # 5️⃣ Default → out of scope (SAFE DEFAULT)
    return "out_of_scope"
