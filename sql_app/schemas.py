from pydantic import BaseModel
from typing import List


#TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


#USER
class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class UserCreat(User):
    password: str


#TODOS
class TodoBase(BaseModel):
    title: str
    description: str | None = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    pass

    class Config:
        orm_mode = True


#TEXT
class TextBase(BaseModel):
    text:str

class TextCreate(TextBase):
    pass

class Text(TextBase):
    user:str

    class Config:
        orm_mode = True      


#MESSAGE
class MessageBase(BaseModel):
    message:str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    pass

    class Config:
        orm_mode = True    
     