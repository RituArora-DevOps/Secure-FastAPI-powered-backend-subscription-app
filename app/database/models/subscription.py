from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..connection import Base
from datetime import datetime, timezone

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc)) # why lambda? Because SQLAlchemy needs a callable (something it can call each time a new row is inserted). If we just write datetime.now(timezone.utc), it will evaluate once at import time.
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")