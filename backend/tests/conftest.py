# The "Magic" setup file
# Force SQLAlchemy to use a dfferent database URL for tests
# Override FastAPI get_db dependency so the app uses the test session
# Wipe and recreate all tables before each test to ensure isolation

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.connection import Base, get_db
from fastapi.testclient import TestClient
from app.database.models.user import User
from app.utils import hash_password

# 1. Use a seperate TEST database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@172.24.98.77:5432/subscription_engine_test"

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
def client(db_session):
    # Dependency override logic
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def user_token(client):
    """Creates a normal user and returns their Bearer Token."""
    client.post("/users/", json={
        "email": "user@test.com",
        "name": "Test User",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "user@test.com",
        "password": "testpassword"
    })
    return response.json()["access_token"]

@pytest.fixture
def admin_token(client, db_session):
    """Creates an admin user and returns their Bearer Token."""
    # We bypass the API to create the frst admin directly in the DB
    admin = User(email="admin@test.com", name="Admin User", hashed_password=hash_password("adminpassword"), is_admin=True)
    db_session.add(admin)
    db_session.commit()

    response = client.post("/auth/login", data={
        "username": "admin@test.com",
        "password": "adminpassword"
    })

    return response.json()["access_token"]
