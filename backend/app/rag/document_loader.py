import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(filepath: str, project_id: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError("PDF file not found.")
        
    loader = PyPDFLoader(filepath)
    docs = loader.load()
    
    # Add metadata
    for doc in docs:
        doc.metadata["project_id"] = project_id
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits
