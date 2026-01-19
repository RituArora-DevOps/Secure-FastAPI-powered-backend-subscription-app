# Models = database layer (internal representation of data)
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..connection import Base
from datetime import datetime, timezone

from .subscription import Subscription

# Users and Subscriptions tables - reprsesnts the DB tables
# Models define the structure of the database tables and their relationships
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    subscriptions = relationship("Subscription", back_populates="user")

