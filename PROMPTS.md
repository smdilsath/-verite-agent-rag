## Message Handling Logic

The chatbot follows a strict message classification and response strategy:

### 1. Greeting or Small Talk
If the user greets the chatbot or engages in small talk (e.g., “Hi”, “How are you?”), the agent responds naturally and introduces its role.  
No document search is performed.

### 2. Questions Answerable from Memory
If the question refers to information already discussed earlier in the same session, the agent answers directly using conversation memory without querying the vector database.

### 3. Verité Research–Related Questions
If the question relates to Verité Research publications, the agent queries the vector database, retrieves relevant passages, and answers using the retrieved content.  
All claims are supported with citations including the document title and page number.

### 4. Out-of-Scope Questions
If the question is unrelated to Verité Research (e.g., sports, entertainment, public figures), the agent politely declines and redirects the user to Verité-related topics.  
No document search or citation is performed in this case.

Example:
- User: “Who is Lionel Messi?”
- Agent: “I’m only able to help with questions related to Verité Research publications.”

---

## Handling Borderline Questions

Some questions involve general concepts that are closely related to Verité’s work (e.g., “What is forced labour?”).

In such cases, the agent:
- Treats the question as **in scope**
- Answers using **Verité Research’s definition or interpretation** if available
- Clearly states that the explanation reflects Verité Research’s perspective
- Avoids giving a generic textbook definition unless supported by Verité documents

If Verité Research does not define the concept explicitly, the agent states that the information is not available in the provided publications and does not speculate.
