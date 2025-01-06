from fastapi import FastAPI
from api import user
from db.session import engine
from models.user import Base

# Create FastAPI instance
app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router)
