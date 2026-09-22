import os
from langchain_community.vectorstores import FAISS
from app.rag.vector_store import get_embeddings, VECTOR_STORE_PATH

def retrieve_knowledge(query: str, project_id: str, k: int = 3):
    if not os.path.exists(VECTOR_STORE_PATH):
        return "No knowledge base configured yet."
        
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # We can filter by project_id using FAISS metadata filtering
    docs = vector_store.similarity_search(
        query, 
        k=k, 
        filter={"project_id": project_id}
    )
    
    if not docs:
        return "No relevant documents found in this project's knowledge base."
        
    res = []
    for d in docs:
        res.append(d.page_content)
        
    return "\n\n---\n\n".join(res)
