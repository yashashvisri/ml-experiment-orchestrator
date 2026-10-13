import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.report_service import ReportService
from app.schemas.report import ReportSummaryResponse

router = APIRouter()

@router.get("/{project_id}/summary", response_model=ReportSummaryResponse)
def get_report_summary(
    project_id: str,
    experiment_id: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        p_uuid = uuid.UUID(project_id)
        e_uuid = uuid.UUID(experiment_id) if experiment_id else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    metrics_data, _, markdown_text = ReportService.generate_report_content(db, p_uuid, e_uuid, current_user)
    best = metrics_data.get("best_run")
    
    return ReportSummaryResponse(
        project_id=str(project_id),
        project_name=metrics_data["project"]["name"],
        experiment_name=metrics_data["experiments"][0]["name"] if metrics_data["experiments"] else None,
        total_runs=metrics_data["total_runs"],
        best_model_name=best.get("name") if best else None,
        best_metric=best.get("metrics") if best else None,
        markdown_content=markdown_text
    )
