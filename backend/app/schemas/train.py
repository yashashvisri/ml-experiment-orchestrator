from uuid import UUID
from pydantic import BaseModel

class TrainRequest(BaseModel):
    dataset_id: UUID
    target_column: str
    model_type: str
    n_trials: int = 10
