from pydantic import BaseModel
from fastapi import WebSocket
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
    id: int
    owner_id: int

    class Config:
        orm_mode = True


#TEXT
class TextBase(BaseModel):
    text:str

class TextCreate(TextBase):
    pass

class Text(TextBase):
    id : int
    owner_id: int

    class Config:
        orm_mode = True      

"""
#CONECTION MANAGER FOR WEBSOCKETS
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            """