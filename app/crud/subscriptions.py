from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from ..database import models, schemas

def create_subscription(db: Session, sub: schemas.SubscriptionCreate, user_id: int):
    # 1. Validate plan ID
    plan = db.query(models.Plan).filter(models.Plan.id == sub.plan_id, models.Plan.is_active == True).first()

    if not plan:
        return None # The route handles the 404/400 error
    
    # set start/end date based on plan duration
    start_date = datetime.now(timezone.utc)
    end_date = start_date + relativedelta(months=plan.duration_months)

    db_sub = models.Subscription(plan_id=sub.plan_id, start_date=start_date, end_date=end_date, is_active=True, user_id=user_id)
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

# Fetch all foer a specific user
def get_subscriptions_by_user(db: Session, user_id: int):
    return db.query(models.Subscription).filter(models.Subscription.user_id == user_id).all()

# Fetch one specific record
def get_subscriptions_by_id(db:Session, subsub_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subsub_id).first() # Fetch a specific subscription by its ID

# Fetch everything for admin
def get_all_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def update_subscription_end_date(db: Session, sub_id: int, new_end_date: datetime):
    # Useful for Admins extending a user's access
    db_sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id).first()
    if db_sub:
        db_sub.end_date = new_end_date
        db.commit()
        db.refresh(db_sub)
    return db_sub

def hard_delete_subscription(db: Session, sub_id: int):
    db_sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id).first()
    if db_sub:
        db.delete(db_sub)
        db.commit()
        return True
    return False    

def cancel_subscription(db: Session, sub_id: int):
    sub = db.query(models.Subscription).filter(models.Subscription.id == sub_id).first()
    if sub:
        sub.is_active = False
        # sub.end_date = datetime.now(timezone.utc)
        db.commit()
        db.refresh(sub)
    return sub

