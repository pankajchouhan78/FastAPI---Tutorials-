# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# import os

# from schemas import TokenData
# from database import SessionLocal
# from models import User

# SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_password_hash(password: str):
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return TokenData(**payload)
#     except JWTError:
#         return None


from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from schemas import TokenData
from database import SessionLocal
from models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize OAuth2PasswordBearer for token extraction from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)  # Create TokenData object from payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )
    
    # Verify token and get user ID from the token payload
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.id).first()  # Retrieve user by ID from DB
    if user is None:
        raise credentials_exception
    return user

