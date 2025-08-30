import datetime
from pydantic import BaseModel


class PlanBase(BaseModel):
    name: str
    price: float
    description: str | None = None
    duration_months: int
 
 # For creating a new plan
    # When a client creates a plan, they don't provide an ID or is_active
class PlanCreate(PlanBase):
    pass

# For reading plan data (response model)
# This is what we return to the client after creating/fetching a plan
class Plan(PlanBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True  # Tells Pydantic to work with ORM objects and read data from SQLAlchemy objects
