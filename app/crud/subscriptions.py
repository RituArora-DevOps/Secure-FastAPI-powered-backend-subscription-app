from sqlalchemy.orm import Session
from .. import models, schemas

def create_subscription(db: Session, sub: schemas.SubscriptionCreate, user_id: int):
    db_sub = models.Subscription(**sub.dict(), user_id=user_id)
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def get_subscription(db: Session, user_id: int):
    return db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()

