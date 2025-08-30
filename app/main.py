from fastapi import FastAPI
from .routers import users, subscriptions
from .database.connection import engine
from .database.models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Subscription Management API")

app.include_router(users.router)
app.include_router(subscriptions.router)