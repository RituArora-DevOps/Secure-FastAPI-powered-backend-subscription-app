from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class PlanBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: float
    description: str | None = None
    duration_months: int
 
 # For creating a new plan
    # When a client creates a plan, they don't provide an ID or is_active
class PlanCreate(PlanBase):
    pass

# For updating an existing plan
class PlanUpdate(PlanBase):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    duration_months: Optional[int] = None

# For reading plan data (response model)
# This is what we return to the client after creating/fetching a plan
class Plan(PlanBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    