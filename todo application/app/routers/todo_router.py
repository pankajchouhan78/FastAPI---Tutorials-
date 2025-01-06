from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, auth
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)

# More endpoints for CRUD operations on Todo can be added


@router.get('/todos/')
def data():
    return {"data":"hello world"}
