from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine (connection)
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Dependency to get DB session
# This function open/close sessions properly 
# This opens a session for a request and closes it when the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()