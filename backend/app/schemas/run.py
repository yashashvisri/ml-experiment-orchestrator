from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class RunBase(BaseModel):
    name: str

class RunCreate(RunBase):
    pass

class RunResponse(RunBase):
    id: UUID
    mlflow_run_id: str
    experiment_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
