# VeriBot 🤖 — Agentic RAG Chatbot for Verité Research

VeriBot is an agentic AI chatbot that allows users to ask questions about Verité Research publications.
It uses Retrieval-Augmented Generation (RAG), conversation memory, and intent-based routing to answer questions accurately and responsibly.

---

## 🔗 Live Demo
https://dilsath-verite-agent-rag.hf.space/

---

## 🧠 Features
- Agentic routing (decides when to search vs respond from memory)
- FAISS vector database for document retrieval
- Session-based conversation memory
- Polite refusal for out-of-scope questions
- Clear document citations (title + page number)
- Deployed on Hugging Face Spaces

---



---

## 🛠️ Setup Instructions

### 1. Clone repository
```bash
1.git clone https://github.com/smdilsath/-verite-agent-rag.git
2.cd verite-agent-rag

3.python -m venv venv
4.source venv/bin/activate  # Windows: venv\Scripts\activate
5.pip install -r requirements.txt

7.python rag/ingest.py
8.streamlit run app.py

