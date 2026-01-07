from ..database.schemas import plan as plan_schemas
from ..database import models
from sqlalchemy.orm import Session

def create_plan(db: Session, plan: plan_schemas.PlanCreate):
    db_plan = models.Plan(
        name=plan.name, 
        price=plan.price, 
        description=plan.description,
        duration_months=plan.duration_months
        )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def update_plan(db: Session, plan_id: int, plan: plan_schemas.PlanUpdate):
    db_plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if db_plan:
        # db_plan.name = plan.name
        # db_plan.price = plan.price
        # db_plan.description = plan.description
        # db_plan.duration_months = plan.duration_months
        for key, value in plan.model_dump(exclude_unset=True).items():
            setattr(db_plan, key, value)
        db.commit()
        db.refresh(db_plan)
    return db_plan

def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()

def get_plans(db: Session, active_only: bool = False):
    query = db.query(models.Plan)
    if active_only:
        query = query.filter(models.Plan.is_active == True)
    return query.all()

def deactivate_plan(db: Session, plan_id: int):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if plan:
        plan.is_active = False
        db.commit()
        db.refresh(plan)
    return plan

def delete_plan(db: Session, plan_id: int):
    db_plan = get_plan(db, plan_id)
    if db_plan:
        db.delete(db_plan)
        db.commit()
        return True
    return False