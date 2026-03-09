from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

DATA_PATH = "data"

docs = []

for file in os.listdir(DATA_PATH):

    if file.endswith(".pdf"):

        loader = PyPDFLoader(os.path.join(DATA_PATH, file))
        docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(chunks, embeddings)

db.save_local("vectorstore")

print("Vector DB created.")