# Schemas = API layer (external representation of data)
# request/response flow in FastAPI - request JSON → schema → model → DB → back to schema → response JSON
# Schemas use Pydantic to define the structure of request and response bodies
# Represents the API request and response shapes
# Define how data is validated and exposed to clients
from pydantic import BaseModel, EmailStr

from .subscription import Subscription

# These are the core fields needed for any user, whether creating or reading
class UserBase(BaseModel):
    email: EmailStr
    name: str

# For creating a new user
# When a client creates a user, they provide email, name
# Request body for POST /users/
class UserCreate(UserBase):
    hashed_password: str

# For reading user data (response model)
# This is what we return to the client after creating/fetching a user
class User(UserBase):
    id: int
    is_active: bool
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True

