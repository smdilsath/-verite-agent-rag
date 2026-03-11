# agent/intent.py

def classify_intent(text: str) -> str:
    t = text.lower().strip()

    # Greeting
    if t in {"hi", "hello", "hey"}:
        return "greeting"

    # Small talk
    if "how are you" in t or "thank you" in t:
        return "smalltalk"

    # Follow-up / memory-based questions
    follow_ups = [
        "which publication",
        "which report",
        "which document",
        "what page",
        "cite",
        "source",
        "that",
    ]
    if any(p in t for p in follow_ups):
        return "verite_query"

    # Verité-related keywords
    verite_keywords = [
        "verité",
        "rti",
        "proactive disclosure",
        "beneficial ownership",
        "forced labour",
        "public authority",
    ]
    if any(k in t for k in verite_keywords):
        return "verite_query"

    # Otherwise → out of scope
    return "out_of_scope"
