from fastapi import APIRouter,Depends,HTTPException
from models import Item
from database import get_db
from schemas import ItemResponse,ItemCreate,ItemUpdate,Decoded_Token
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from starlette import status
from routers.auth import get_current_user

router = APIRouter(prefix="/items",tags=["items"])

DbDependency = Annotated[Session,Depends(get_db)]
userDependency = Annotated[Decoded_Token,Depends(get_current_user)]

@router.get("",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_all(db :Session = Depends(get_db)):
    found_item = db.query(Item).order_by(Item.id).all()
    return found_item

@router.get("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_id(id :int,user :userDependency,db :Session = Depends(get_db)):
   user_id = user.user_id
   found_item = db.query(Item).filter(Item.id == id).filter(Item.user_id ==user_id).first()
   if found_item is None:
       raise HTTPException(status_code=404,detail="Item not found")
   return found_item
       

@router.get("/",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_name(name :str,db :Session = Depends(get_db)):
    found_item = db.query(Item).filter(Item.name == name).all()
    if not found_item:
        raise HTTPException(status_code=404,detail="Item not found")
    return found_item


@router.post("",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
async def create(create_item :ItemCreate,user :userDependency,db :Session = Depends(get_db)):
    user_id = user.user_id
    new_item = Item(
        **create_item.model_dump(),user_id=user_id
    )
    db.add(new_item)
    db.commit()
    return new_item


@router.put("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def update(id :int,update_item :ItemUpdate,user :userDependency,db :Session=Depends(get_db)):
    user_id = user.user_id
    item = db.query(Item).filter(Item.id == id).filter(Item.user_id==user_id).first()
    
    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    
    item.name =item.name if update_item.name is None else update_item.name
    item.email =item.email if update_item.email is None else update_item.email

    db.add(item)
    db.commit()
    return item
            
        
@router.delete("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def deleate(id :int,user :userDependency,db :Session=Depends(get_db)):

    item = await find_by_id(id,user,db)

    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    db.delete(item)
    db.commit()
    return item