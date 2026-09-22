import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.core.config import settings
from app.rag.document_loader import load_and_chunk_pdf
from app.rag.vector_store import add_documents_to_store

router = APIRouter()

@router.post("/{project_id}/documents")
def upload_knowledge_document(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify project
    project = ProjectRepository.get_by_id(db, uuid.UUID(project_id))
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for now.")

    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Process RAG
    try:
        docs = load_and_chunk_pdf(file_path, project_id)
        add_documents_to_store(docs)
        return {"message": f"Successfully indexed {len(docs)} chunks from {file.filename}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
