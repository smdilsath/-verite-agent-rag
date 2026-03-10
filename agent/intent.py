# agent/intent.py

def classify_intent(user_input: str) -> str:
    text = user_input.lower().strip()

    greetings = ["hi", "hello", "hey"]
    smalltalk = ["how are you", "who are you", "what can you do"]

    if any(text.startswith(g) for g in greetings):
        return "greeting"

    if any(x in text for x in smalltalk):
        return "smalltalk"

    out_of_scope = [
        "virat kohli", "cricket", "football",
        "movie", "actor", "weather", "bitcoin"
    ]

    if any(x in text for x in out_of_scope):
        return "out_of_scope"

    # Borderline but Verité-relevant concepts
    verite_concepts = [
        "forced labour", "forced labor",
        "governance", "public finance",
        "labour rights", "debt", "imf"
    ]

    if any(x in text for x in verite_concepts):
        return "verite_query"

    return "verite_query"
