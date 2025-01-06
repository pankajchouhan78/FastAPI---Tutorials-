from fastapi import FastAPI
from routers import auth_router, todo_router
from database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(todo_router.router, prefix="/todos", tags=["todos"])
