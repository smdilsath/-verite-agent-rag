def detect_intent(message):

    message = message.lower()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    smalltalk = ["how are you", "what can you do", "who are you"]
    followup_words = ["that", "this", "it", "they", "those", "them"]

    # Greeting
    if any(word in message for word in greetings):
        return "greeting"

    # Small talk
    if any(word in message for word in smalltalk):
        return "smalltalk"

    # Follow-up question
    if any(word in message.split() for word in followup_words):
        return "followup"

    # Verité related topics
    verite_keywords = [
        "verite",
        "forced labour",
        "labour",
        "governance",
        "policy",
        "fiscal",
        "public finance",
        "research",
        "sri lanka"
    ]

    if any(word in message for word in verite_keywords):
        return "verite_query"

    return "unknown"