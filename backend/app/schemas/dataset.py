from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DatasetBase(BaseModel):
    name: str
    description: str | None = None


class DatasetCreate(DatasetBase):
    pass


class DatasetResponse(DatasetBase):
    id: UUID
    file_path: str
    file_size: int
    project_id: UUID
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
