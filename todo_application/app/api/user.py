from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user import User
from auth.register import hash_password, verify_password
from auth.azure_ad import AzureADAuth
from config import Config
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import JWTError, jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Token Generation
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

# User Registration API
@router.post("/register/")
async def register_user(email: str, password: str, first_name: str, last_name: str, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(password)
    user = User(email=email, hashed_password=hashed_password, first_name=first_name, last_name=last_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"msg": "User registered successfully"}

# User Login API
@router.post("/login/")
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# List Users (Authenticated)
@router.get("/users/")
async def get_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    azure_auth = AzureADAuth()
    user_info = azure_auth.get_user_info(token)
    
    users = db.query(User).all()
    return users
