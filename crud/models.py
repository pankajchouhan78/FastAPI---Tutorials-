"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from db_connect import *

# define the base model class
Base = declarative_base()

# Define the base user model

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
Base.metadata.crete_all(bind=True)

"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from db_connect import engine

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)


Base.metadata.create_all(engine)