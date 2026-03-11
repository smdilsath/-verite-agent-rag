# rag/ingest.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"

# 👈 ADD THIS: filename → publication title
PDF_TITLES = {
    "21082025_ProactiveDisclosure.pdf": "Proactive Disclosure Under the RTI Act in Sri Lanka: Ranking Key Public Authorities in 2024",
    "beneficial_ownership.pdf": "Proposed Beneficial Ownership Register: Two Gaps Undermine Effectiveness",
    "cigarette_tax.pdf": "Stealth Reduction of Cigarette Tax Rates",
    "primary_expenditure_rule.pdf": "1.3% Primary Expenditure Rule Proposed for Sri Lanka Departs from Economic Theory and Practice",
    "forensic_audit_epf.pdf": "Forensic Audit of Central Bank 2019: Assessment of Losses to the EPF",
}

def ingest_documents():
    print("🔄 Ingesting Verité PDFs...")

    if not os.path.isdir(DATA_DIR):
        raise RuntimeError("❌ data/ folder not found. Upload PDFs in Hugging Face.")

    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

    if not pdf_files:
        raise RuntimeError("❌ No PDF files found in data/ folder.")

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = []

    for file in pdf_files:
        file_path = os.path.join(DATA_DIR, file)
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        for p in pages:
            p.metadata["source"] = file
            p.metadata["title"] = PDF_TITLES.get(file, file)  # 👈 ADD THIS
            documents.append(p)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise RuntimeError("❌ No text extracted from PDFs.")

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTORSTORE_DIR)

    print("✅ Vectorstore created successfully")

if __name__ == "__main__":
    ingest_documents()
