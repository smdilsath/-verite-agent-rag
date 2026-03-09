from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings

VECTOR_PATH = "vectorstore"

def load_vectorstore():

    embeddings = get_embeddings()

    db = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db