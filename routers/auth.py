from fastapi import APIRouter,Depends,Request,HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schemas import Decoded_Token,UserCreate,UserResponse,Token
from models import User
from starlette import status
import hashlib
import base64
import os
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth",tags={"auth"})

DbDependency = Annotated[Session,Depends(get_db)]
OAuth2schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token :Annotated[str,Depends(OAuth2schema)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGOLITHM)
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            return None
        return Decoded_Token(username=username,user_id=user_id)
    except JWTError:
        raise JWTError
    
userDependency = Annotated[Decoded_Token,Depends(get_current_user)]
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]


@router.post("/signup",response_model=UserResponse)
async def create_user(user_create :UserCreate,db :DbDependency):
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac("sha256",user_create.password.encode(),salt,1000).hex()
    new_user = User(
        name = user_create.name,
        password = hashed_password,
        salt = salt.decode()
    )
    
    # new_user = User(**user_create.model_dump())
    db.add(new_user)
    db.commit()
    return new_user


ALGOLITHM = "HS256"
SECRET_KEY = "c9a3524915b0438d9b93044390529e5dffa3edfad83b8de11bad6593beb8104d"
def create_access_token(username :str,user_id :int,expires_delta :timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub" :username,"id" :user_id,"exp" :expires}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGOLITHM)

@router.post("/login",status_code=status.HTTP_200_OK,response_model=Token)
async def login(db :DbDependency,form_data :FormDependency):
    username = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.name==username).first()
    if not user:
        raise HTTPException(status_code=400,detail="Incorrect username ")
    hashed_password = hashlib.pbkdf2_hmac("sha256",password.encode(),user.salt.encode(),1000).hex()
    # データベースから取得したsaltをエンコードしたものと比較する
    if user.password != hashed_password:
        raise HTTPException(status_code=400,detail="Incorrect password")
    
    token = create_access_token(user.name,user.id,timedelta(minutes=20))
    return {"access_token" :token,"token_type" :"bearer"}


