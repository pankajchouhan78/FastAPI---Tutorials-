from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, auth
from models import User
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": db_user.username, "id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
