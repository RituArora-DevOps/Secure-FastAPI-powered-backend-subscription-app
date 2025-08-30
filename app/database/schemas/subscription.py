from datetime import datetime 
from typing import Optional
from pydantic import BaseModel

# These are the core fields needed for any subscription, whether creating or reading
class SubscriptionBase(BaseModel):
    plan_id: int

# For creating a new subscription
# When a client creates a subscription, they don't provide an ID or user_id or is_active
class SubscriptionCreate(SubscriptionBase):
    pass

# For reading subscription data (response model)
# This is what we return to the client after creating/fetching a subscription
class Subscription(SubscriptionBase):
    id: int
    user_id: int
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool


    class Config:
        orm_mode = True # Tells Pydantic to work with ORM objects and read data from SQLAlchemy objects