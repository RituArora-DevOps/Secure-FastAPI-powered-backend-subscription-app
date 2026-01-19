from sqlalchemy.orm import Session

from ..utils import hash_password
from ..database.models.user import User 
from ..database.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, hashed_password=hash_password(user.password), name=user.name)
    db.add(db_user) 
    db.commit() 
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all() # Fetch multiple users with pagination

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        db.commit() 
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

