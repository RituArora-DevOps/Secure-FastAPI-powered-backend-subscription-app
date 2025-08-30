
from xmlrpc.client import Boolean
from ..connection import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime, DateTime, timezone

class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # e.g. Basic, Standard, Premium
    price = Column(Integer, nullable=False)  # e.g. 9.99
    description = Column(String, nullable=True)
    duration_months = Column(Integer, nullable=False)  # Duration in months
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    subscriptions = relationship("Subscription", back_populates="plan")