memory = []

def add_memory(user, bot):
    memory.append({
        "user": user,
        "bot": bot
    })

def get_memory():
    history = ""

    for m in memory[-5:]:
        history += f"User: {m['user']}\nAssistant: {m['bot']}\n"

    return history