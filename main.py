from fastapi import FastAPI,Body,Depends,HTTPException
from schemas import ItemCreate,ItemUpdate,ItemResponse
from database import get_data
from typing import Optional
from sqlalchemy.orm import Session
from models import Item

app = FastAPI()

items = [
  {"id":1,"name":"tanaka1","email":"nhkh@com"},
  {"id":2,"name":"tanaka2","email":"nhkh@com"},
  {"id":3,"name":"tanaka3","email":"nhkh@com"},
]

#READ処理

@app.get("/items",response_model=list[ItemResponse])
async def find_all(db :Session = Depends(get_data)):
    return db.query(Item).order_by(Item.id).all()


@app.get("/items/{id}",response_model=Optional[ItemResponse])
async def find_by_id(id :int,db :Session = Depends(get_data)):
   found_item = db.query(Item).filter(Item.id == id).first()
   if found_item is None:
       raise HTTPException(status_code=404,detail="Item not found")
   return found_item
       

@app.get("/items/",response_model=list[ItemResponse])
async def find_by_name(name :str,db :Session = Depends(get_data)):
    found_item = db.query(Item).filter(Item.name == name).all()
    if not found_item:
        raise HTTPException(status_code=404,detail="Item not found")
    return found_item


@app.post("/items",response_model=ItemResponse)
async def create(create_item :ItemCreate,db :Session = Depends(get_data)):
    new_item = Item(
        **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item


@app.put("/items/{id}",response_model=Optional[ItemResponse])
async def update(id :int,update_item :ItemUpdate,db :Session=Depends(get_data)):
    
    item = db.query(Item).filter(Item.id == id).first()
    
    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    
    item.name =item.name if update_item.name is None else update_item.name
    item.email =item.email if update_item.email is None else update_item.email

    db.add(item)
    db.commit()
    return item
            
        
@app.delete("/items/{id}",response_model=Optional[ItemResponse])
async def deleate(id :int,db :Session=Depends(get_data)):

    item = await find_by_id(id,db)

    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    db.delete(item)
    db.commit()
    return item