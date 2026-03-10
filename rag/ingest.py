# rag/ingest.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"


def ingest_documents():
    print("🔄 Ingesting Verité PDFs...")

    # 1️⃣ Ensure data/ exists (HF requirement)
    if not os.path.isdir(DATA_DIR):
        raise RuntimeError("❌ data/ folder not found. Upload PDFs in Hugging Face.")

    pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

    if not pdf_files:
        raise RuntimeError("❌ No PDF files found in data/ folder.")

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    # 2️⃣ Embeddings (small + HF-safe)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = []

    # 3️⃣ Load PDFs and FORCE source metadata
    for file in pdf_files:
        file_path = os.path.join(DATA_DIR, file)
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        for p in pages:
            p.metadata["source"] = file   # ✅ critical for citation
            documents.append(p)

    # 4️⃣ Chunk documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise RuntimeError("❌ No text extracted from PDFs.")

    # 5️⃣ Create and save FAISS index
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTORSTORE_DIR)

    print("✅ Vectorstore created successfully")
    print(f"📄 Documents indexed: {len(pdf_files)}")
    print(f"🧩 Chunks created: {len(chunks)}")


# 6️⃣ Allow manual execution (optional)
if __name__ == "__main__":
    ingest_documents()
