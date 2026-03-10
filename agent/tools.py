# agent/tools.py
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from rag.ingest import ingest_documents

VECTORSTORE_PATH = "vectorstore"

EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_or_create_vectorstore():
    """
    Lazy-load FAISS.
    Create it if missing (Hugging Face safe).
    """

    if not os.path.exists(VECTORSTORE_PATH):
        print("⚠️ Vectorstore missing. Running ingestion...")
        ingest_documents()

    return FAISS.load_local(
        VECTORSTORE_PATH,
        EMBEDDINGS,
        allow_dangerous_deserialization=True
    )

def search_verite(query, k=4):
    db = load_or_create_vectorstore()
    return db.similarity_search(query, k=k)
