from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List


#BINDING DATABASE
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


#SECURITY
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user( db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token/", response_model=schemas.Token)
async def login_for_access_token( db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud. authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#CREATING A USER
@app.post("/users/")
def create_user(
    user: schemas.UserCreat, db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)


#CREATING AND SEEING TODOS
@app.post("/createtodos/", response_model=schemas.Todo)
def create_todo_for_user(
    todo: schemas.TodoCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)

@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    todos = crud.get_todos(db,current_user.id)
    return todos


#CREATING AND SEEING TEXT FOR GROUP CHAT
@app.post("/sendtext/", response_model=schemas.Text)
def send_text_to_group(text: schemas.TextCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.create_user_text(db=db, text=text, user_id=current_user.id)

@app.get("/groupchat/", response_model=list[schemas.Text])
def group_chat(db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    text = crud.get_text(db)
    return text
