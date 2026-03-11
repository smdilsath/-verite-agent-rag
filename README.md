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

## 📚 Knowledge Base (5 Verité Publications)

1. **Proposed Beneficial Ownership Register: Two Gaps Undermine Effectiveness** (2024)  
   https://www.veriteresearch.org/publication/proposed-beneficial-ownership-register-two-gaps-undermine-effectiveness/

2. **Stealth Reduction of Cigarette Tax Rates** (2023)  
   https://www.veriteresearch.org/publication/stealth-reduction-of-cigarette-tax-rates/

3. **1.3% Primary Expenditure Rule Proposed for Sri Lanka Departs from Economic Theory and Practice** (2024)  
   https://www.veriteresearch.org/publication/13-primary-expenditure-rule-proposed-for-sri-lanka-departs-from-economic-theory-and-practice/

4. **Proactive Disclosure Under the RTI Act in Sri Lanka: Ranking Key Public Authorities in 2024** (2024)  
   https://www.veriteresearch.org/publication/proactive-disclosure-under-the-rti-act-in-sri-lanka-ranking-key-public-authorities-in-2024/

5. **Forensic Audit of Central Bank 2019: Assessment of Losses to the EPF** (2023)  
   https://www.veriteresearch.org/publication/forensic-audit-of-central-bank-2019-assessment-of-losses-to-the-epf/

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

