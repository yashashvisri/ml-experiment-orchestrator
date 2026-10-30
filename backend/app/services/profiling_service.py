import os
import uuid
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.project_repository import ProjectRepository
from app.repositories.dataset_repository import DatasetRepository
from app.models.user import User
from app.profiling.stats_extractor import extract_summary_stats
from app.profiling.column_profiler import profile_columns
from app.profiling.correlation_analyzer import compute_correlation_matrix
from app.profiling.target_detector import analyze_target_candidate
from app.profiling.ai_advisor import generate_ai_dataset_advice
from app.schemas.profiling import DatasetProfileResponse

class ProfilingService:
    @staticmethod
    def profile_dataset(db: Session, project_id: uuid.UUID, dataset_id: uuid.UUID, current_user: User) -> DatasetProfileResponse:
        project = ProjectRepository.get_by_id(db, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")

        dataset = DatasetRepository.get_by_id(db, dataset_id)
        if not dataset or dataset.project_id != project_id:
            raise HTTPException(status_code=404, detail="Dataset not found")

        if not os.path.exists(dataset.file_path):
            raise HTTPException(status_code=404, detail="Dataset file missing on disk")

        try:
            df = pd.read_csv(dataset.file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read CSV dataset: {str(e)}")

        summary = extract_summary_stats(df)
        columns = profile_columns(df)
        correlation = compute_correlation_matrix(df)
        target_info = analyze_target_candidate(df)
        ai_recommendations = generate_ai_dataset_advice(summary, columns, target_info)

        return DatasetProfileResponse(
            dataset_id=str(dataset.id),
            dataset_name=dataset.name,
            summary=summary,
            columns=columns,
            correlation=correlation,
            ai_recommendations=ai_recommendations
        )
