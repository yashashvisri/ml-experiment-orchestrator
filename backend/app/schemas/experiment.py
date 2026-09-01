from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ExperimentBase(BaseModel):
    name: str
    description: str | None = None

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ExperimentResponse(ExperimentBase):
    id: UUID
    mlflow_experiment_id: str
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
