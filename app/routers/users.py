from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from ..database import connection

from ..crud import crud
from ..database.schemas import user

# Routers = application layer (entry point for API requests)
# Define the API endpoints and route requests to the appropriate services
router = APIRouter(prefix="/users", tags=["users"])

# Dependency to get DB session
def get_db():
    db=connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Here we will define user-related endpoints (e.g., create user, get user, update user, delete user)
# Each endpoint will interact with the database via SQLAlchemy models and sessions
# and will use Pydantic schemas for request validation and response formatting

@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=user.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db)