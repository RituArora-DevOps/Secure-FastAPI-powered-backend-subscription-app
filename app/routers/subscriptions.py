from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from ..database import connection

from ..crud import crud
from ..database.schemas import user

# Routers = application layer (entry point for API requests)
router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


# Dependency to get DB session
def get_db():

    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Here we will define subscription-related endpoints (e.g., create subscription, get subscription)
# Each endpoint will interact with the database via SQLAlchemy models and sessions
# and will use Pydantic schemas for request validation and response formatting
# Placeholder endpoint
@router.post("/{user.id}", response_model=user.Subscription)
def create_subscription(user_id: int, sub: user.SubscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_subscription(db, sub, user_id)

@router.get("/{user.id}", response_model=user.Subscription)
def get_subscription(user_id: int, db: Session = Depends(get_db)):
    return crud.get_subscription(db, user_id)
