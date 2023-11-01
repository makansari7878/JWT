from datetime import timedelta, datetime
from typing import Annotated
from fastapi import  APIRouter, Depends, HTTPException
from pydantic import  BaseModel
from sqlalchemy.orm import  Session
from starlette import  status
from database import SessionLocal
from models import Users
from passlib.context import  CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter( prefix='/auth',tags=['auth'])

SECRET_KEY = '12345abcdexyz789'
ALOGRITHM = 'HS256'

bcyrpt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

#auth is our file and token is the endpoing
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#-------------------------

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency, create_user_request : CreateUserRequest):
    create_user_model = Users( username=create_user_request.username,
                               password=  create_user_request.password)
    db.add(create_user_model)
    db.commit()


#to check whether username n pwd is present in db
def autheticate_user(username:str, mypassword:str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return  False
    pwd = db.query(Users).filter(Users.password == mypassword).first()
    if not pwd:
        return False
    return user

def create_access_token(username : str, userid : int, expires_delta:timedelta):
    encode = {'sub':username, 'id':userid}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALOGRITHM)


@router.post('/token',response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db:db_dependency):
    user = autheticate_user(form_data.username, form_data.password,db)
    if not user:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access token':token, 'token_type':'bearer'}