from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Store hashed password
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default="user")  # e.g. user, admin
