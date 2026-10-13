import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.project_repository import ProjectRepository
from app.reporting.metrics_collector import collect_experiment_metrics
from app.reporting.ai_synthesizer import synthesize_ai_analysis
from app.reporting.markdown_generator import generate_markdown_report
from app.reporting.pdf_builder import build_pdf_report
from app.models.user import User

class ReportService:
    @staticmethod
    def generate_report_content(db: Session, project_id: uuid.UUID, experiment_id: uuid.UUID | None, current_user: User):
        project = ProjectRepository.get_by_id(db, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")

        metrics_data = collect_experiment_metrics(db, project_id, experiment_id)
        ai_narrative = synthesize_ai_analysis(metrics_data)
        markdown_text = generate_markdown_report(metrics_data, ai_narrative)
        return metrics_data, ai_narrative, markdown_text

    @staticmethod
    def export_pdf(db: Session, project_id: uuid.UUID, experiment_id: uuid.UUID | None, current_user: User) -> bytes:
        metrics_data, ai_narrative, _ = ReportService.generate_report_content(db, project_id, experiment_id, current_user)
        return build_pdf_report(metrics_data, ai_narrative)
