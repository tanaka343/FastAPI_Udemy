from fastapi import FastAPI,Body,Depends,HTTPException,Request
from schemas import ItemCreate,ItemUpdate,ItemResponse,UserCreate,UserResponse,Token,Decoded_Token
from database import get_db
from typing import Optional,Annotated
from sqlalchemy.orm import Session
from models import Item,User
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



app = FastAPI()

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


# デバック用
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.get("/items",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_all(db :Session = Depends(get_db)):
    found_item = db.query(Item).order_by(Item.id).all()
    return found_item


@app.get("/items/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_id(id :int,db :Session = Depends(get_db)):
   found_item = db.query(Item).filter(Item.id == id).first()
   if found_item is None:
       raise HTTPException(status_code=404,detail="Item not found")
   return found_item
       

@app.get("/items/",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_name(name :str,db :Session = Depends(get_db)):
    found_item = db.query(Item).filter(Item.name == name).all()
    if not found_item:
        raise HTTPException(status_code=404,detail="Item not found")
    return found_item


@app.post("/items",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
async def create(create_item :ItemCreate,db :Session = Depends(get_db)):
    new_item = Item(
        **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item


@app.put("/items/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def update(id :int,update_item :ItemUpdate,db :Session=Depends(get_db)):
    
    item = db.query(Item).filter(Item.id == id).first()
    
    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    
    item.name =item.name if update_item.name is None else update_item.name
    item.email =item.email if update_item.email is None else update_item.email

    db.add(item)
    db.commit()
    return item
            
        
@app.delete("/items/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def deleate(id :int,db :Session=Depends(get_db)):

    item = await find_by_id(id,db)

    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    db.delete(item)
    db.commit()
    return item


@app.post("/auth/signup",response_model=UserResponse)
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

@app.post("/auth/login",status_code=status.HTTP_200_OK,response_model=Token)
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


