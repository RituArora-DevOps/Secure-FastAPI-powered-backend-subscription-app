from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..crud import subscriptions as sub_crud
from ..database.schemas import subscription as sub_schemas
from .auth import get_current_user, get_current_admin
from ..database.models.user import User
from ..database.models.subscription import Subscription as sub_model

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=sub_schemas.Subscription)
def create_subscription(
    sub: sub_schemas.SubscriptionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1. Check if they have an active sub (Duplicate check)
    existing_sub = db.query(sub_model).filter(sub_model.user_id==current_user.id, sub_model.is_active==True).first()
    if existing_sub:
        raise HTTPException(status_code=400, detail=f"User with ID {current_user.id} already has an active subscription")
    
    # Now call the CRUD
    # Use current_user.id instead of passing it in the URL
    result = sub_crud.create_subscription(db, sub, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Invalid or inactive plan selected")
    return result

@router.get("/me", response_model=list[sub_schemas.Subscription])
def get_my_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sub_crud.get_subscriptions_by_user(db, current_user.id)

# Admin Route: See every subscription in the system
@router.get("/all", response_model=list[sub_schemas.Subscription])
def read_all_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    # In a real app: if not current_user.is_admin: raise 403  
    return sub_crud.get_all_subscriptions(db)

# ADMIN/USER route: see detail of one
@router.get("/{sub_id}", response_model=sub_schemas.Subscription)
def read_subscription(
    sub_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_sub = sub_crud.get_subscriptions_by_id(db, sub_id)
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Ownership Check
    if db_sub.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    return db_sub

# User/Admin Route: Cancel a subscription
@router.patch("/{subscription_id}/cancel", response_model=sub_schemas.Subscription)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sub = sub_crud.get_subscriptions_by_id(db, subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    # Ownership Check: Only owner or admin can cancel
    if sub.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this subscription")
        
    return sub_crud.cancel_subscription(db, subscription_id)