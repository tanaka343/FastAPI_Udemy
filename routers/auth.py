from fastapi import APIRouter,Depends,Request,HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schemas import Decoded_Token,UserCreate,UserResponse,Token
from models import User
from cruds import auth as auth_cruds
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
# userDependency = Annotated[Decoded_Token,Depends(auth_cruds.get_current_user)]
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]


@router.post("/signup",response_model=UserResponse)
async def create_user(user_create :UserCreate,db :DbDependency):
    return auth_cruds.create_user(user_create,db)



@router.post("/login",status_code=status.HTTP_200_OK,response_model=Token)
async def login(db :DbDependency,form_data :FormDependency):
    username = form_data.username
    password = form_data.password

    user = auth_cruds.login(db,username,password)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or  password")
    
    token = auth_cruds.create_access_token(user.name,user.id,timedelta(minutes=20))
    return {"access_token" :token,"token_type" :"bearer"}


