'''
    Schemas = API layer (external representation of data)
    request/response flow in FastAPI - request JSON → schema → model → DB → back to schema → response JSON
    Schemas use Pydantic to define the structure of request and response bodies
    Represents the API request and response shapes
    Define how data is validated and exposed to clients
    BaseModel - is a data validator / filter - defines how daat moves through the internet
'''
from pydantic import BaseModel, EmailStr, ConfigDict 
from typing import Optional
from .subscription import Subscription

# These are the core fields needed for any user, whether creating or reading
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # SQLAlchemy Model - DB object - uses dot notation (user.email)
    # Pydantic Schema - used to send JSOn to the browser - express data in dict format (user["email"])
    # from_attribute = True helps extract data from db object and turn it into JSON
    email: EmailStr
    name: str

# For creating a new user
# When a client creates a user, they provide email, name
# Request body for POST /users/
class UserCreate(UserBase):
    password: str

# Request body for PUT /users/{id}
# We use Optional so that the user can update just the name, just the email or both
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    model_config = ConfigDict(from_attributes=True)


# For reading user data (response model)
# This is what we return to the client after creating/fetching a user
class User(UserBase):
    id: int
    is_active: bool
    subscriptions: list[Subscription] = []



