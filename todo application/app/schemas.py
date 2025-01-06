# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# class TodoBase(BaseModel):
#     title: str
#     description: Optional[str] = None

# class TodoCreate(TodoBase):
#     pass

# class Todo(TodoBase):
#     id: int
#     is_completed: bool
#     user_id: int

#     class Config:
#         orm_mode = True

# class UserBase(BaseModel):
#     username: str
#     email: str

# class UserCreate(UserBase):
#     password: str

# class User(UserBase):
#     id: int
#     todos: list[Todo] = []

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     id: int

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    is_completed: bool
    user_id: int

    class Config:
        from_attributes = True  # Updated for Pydantic V2

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    todos: list[Todo] = []

    class Config:
        from_attributes = True  # Updated for Pydantic V2

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
