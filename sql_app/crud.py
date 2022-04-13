from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas
from jose import jwt
from passlib.context import CryptContext


#DOING AUTHENTICATION AND CREATING  ACCESS TOKEN
SECRET_KEY = "64d33590225fc1cd874a16d905aff0dcec79694bfbd74904d791cb389a6425d9"

ALGORITHM = "HS256"

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#VERIFING PASSWORD
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


#CREATING AND GETING USER
def create_user(db: Session, user: schemas.UserCreat):
    db_user = models.User(username=user.username,hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()


#CREATING AND GETING USER'S TODOS
def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(db: Session,owner_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id==owner_id).all()


#CREATING AND GETING USER TEXT
def create_user_text(db: Session, text: schemas.TextCreate, username: str):
    db_text = models.Text(**text.dict(), user=username)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text

def get_text(db: Session):
    return db.query(models.Text).all()


#CREATING AND GETING USER Message
def create_user_message(db: Session, message: schemas.MessageCreate, user_id: int,reciver:int):
    db_message = models.Message(**message.dict(), owner_id=user_id,too=reciver)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session,owner_id: int):
    return db.query(models.Message).filter(models.Message.too==owner_id).all()
