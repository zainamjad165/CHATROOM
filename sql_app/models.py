from enum import unique
from sqlalchemy import Boolean,ForeignKey,Column, Integer, String
from .database import Base
from sqlalchemy.orm import relationship

#USER TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
     
    todos = relationship("Todo", back_populates="owner")
    text = relationship("Text", back_populates="owner")


#TODOS TABLE
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")


#TEXT
class Text(Base):
    __tablename__ = "text"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="text")
