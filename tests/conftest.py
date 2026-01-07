# The "Magic" setup file
# Force SQLAlchemy to use a dfferent database URL for tests
# Override FastAPI get_db dependency so the app uses the test session
# Wpe and recreate all tables before each test to ensure isolation

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import Base, get_db
from fastapi.testclient import TestClient

# 1. Use a seperate TEST database
SQLALCHEMY_DATABASE_URL = "postgresql://ossuser:osspass@172.24.98.77:5432/test_db"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='function')
def db_session():
    # Creates tables in the test db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try: 
        yield db # When a function uses yield (a smart return), it becomes generator that produces value one by one (lazy load, unlike return which is an Eager load)
    finally:
        db.close()
        # Drop tables so the next test starts fresh
        Base.metadata.drop_all(bind=engine)

# Client simulates a real browser or mobile app making a request
@pytest.fixture(scope='function')
def  client(db_session):
    # Dependency override logic
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c