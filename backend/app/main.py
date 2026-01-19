# Control Center - The first file that runs when the server is started
# Initialize the application, connect the db and wire up all the modular routes
from fastapi import FastAPI
from .routes import subscription, user, plan, auth
# Importing Engine - the physical connection to Postgres
from .database.connection import engine, Base
# Importing Blueprints (models) so the app knows what tables to create
from .database.models import user as user_model
from .database.models.user import User
from .database.models.plan import Plan
from .database.models.subscription import Subscription

# DB initialization
# This tells SQLAlchemy to look at all the classes that inherits from 'Base' (User, Plan, Subscription)
# and create those tables in the DB, if they don't exist yet. 
user_model.Base.metadata.create_all(bind=engine)

# App initialization - creates the main instance of our web aplication
# The title appears in /docs
app = FastAPI(title="Subscription Management API")

# Rote registration
# Routers are like mini-apps (in our modularized code)
# include_router tells FastAPI - Take all the URLs defined in these files and make them part of the app
app.include_router(user.router)
app.include_router(subscription.router)
app.include_router(plan.router)
app.include_router(auth.router)