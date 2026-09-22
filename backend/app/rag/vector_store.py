import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
from typing import List
from langchain_core.documents import Document

VECTOR_STORE_PATH = os.path.join(settings.UPLOAD_DIR, "faiss_index")

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GEMINI_API_KEY)

def add_documents_to_store(docs: List[Document]):
    embeddings = get_embeddings()
    if os.path.exists(VECTOR_STORE_PATH):
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(docs)
    else:
        vector_store = FAISS.from_documents(docs, embeddings)
        
    vector_store.save_local(VECTOR_STORE_PATH)
