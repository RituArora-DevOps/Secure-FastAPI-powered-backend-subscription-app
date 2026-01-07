from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.models.user import User
from .auth import get_current_admin
from ..database.connection import get_db
from ..crud import plans as plan_crud
from ..database.schemas import plan as plan_schemas

router = APIRouter(prefix="/plans", tags=["plans"])

@router.get("/", response_model=list[plan_schemas.Plan])
def read_plans(db: Session = Depends(get_db)):
    return plan_crud.get_plans(db)

@router.post("/", response_model=plan_schemas.Plan)
def create_plan(
    plan: plan_schemas.PlanCreate, 
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)    
):
    return plan_crud.create_plan(db, plan)

@router.put("/{plan_id}", response_model=plan_schemas.Plan) 
def update_plan(plan_id: int, plan: plan_schemas.PlanUpdate, db: Session = Depends(get_db)):
    updated = plan_crud.update_plan(db, plan_id, plan)
    if not updated:
        raise HTTPException(status_code=404, detail="Plan not found")
    return updated

@router.delete("/{plan_id}", status_code=204)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    success = plan_crud.delete_plan(db, plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return None