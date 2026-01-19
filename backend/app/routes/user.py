from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import connection

from ..crud import users as user_crud
from ..database.schemas import user as user_schema

# Routers = application layer (entry point for API requests)
# Define the API endpoints and route requests to the appropriate services
router = APIRouter(prefix="/users", tags=["users"])

# Here we will define user-related endpoints (e.g., create user, get user, update user, delete user)
# Each endpoint will interact with the database via SQLAlchemy models and sessions
# and will use Pydantic schemas for request validation and response formatting
# Handles user registration route
@router.post("/", response_model=user_schema.User, status_code=201)
def register_user(user: user_schema.UserCreate, db: Session = Depends(connection.get_db)):
    """
    Register a new user in the system.
    Checks if the email is already taken before creating.
    """
    # 1. Check for duplicate email
    existing_user = user_crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Call the CRUD
    return user_crud.create_user(db, user)

@router.get("/{user_id}", response_model=user_schema.User)
def get_user(user_id: int, db: Session = Depends(connection.get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(
    user_id: int, 
    user: user_schema.UserUpdate, 
    db: Session = Depends(connection.get_db)
):
    db_user = user_crud.update_user(db, user_id=user_id, user_update=user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(connection.get_db)):
    success = user_crud.delete_user(db, user_id=user_id)
    if not success: 
        raise HTTPException(status_code=404, detail="User not found")
    return None