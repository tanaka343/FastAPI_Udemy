from fastapi import FastAPI,Body,Depends
from schemas import ItemCreate,ItemUpdate,ItemResponse
from database import get_data
from typing import Optional

app = FastAPI()

items = [
  {"id":1,"name":"tanaka1","email":"nhkh@com"},
  {"id":2,"name":"tanaka2","email":"nhkh@com"},
  {"id":3,"name":"tanaka3","email":"nhkh@com"},
]

#READ処理

@app.get("/items",response_model=list[ItemResponse])
async def find_all():
    return items


@app.get("/items/{id}",response_model=Optional[ItemResponse])
async def find_by_id(id :int):
    for item in items:
        if item["id"]==id:
            return item
        

@app.get("/items/",response_model=list[ItemResponse])
async def find_by_name(name :str):
    filtered_name=[]
    for item in items:
        if name in item["name"]:
            filtered_name.append(item)
    return filtered_name



@app.post("/items",response_model=ItemResponse)
async def create(create_item :ItemCreate):
    new_item={
        "id":len(items)+1,
        "name":create_item.name,
        "email":create_item.email,
    }
    items.append(new_item)
    return new_item

@app.put("/items/{id}",response_model=Optional[ItemResponse])
async def update(id :int,update_item :ItemUpdate):
    for item in items:
        if item["id"]==id:
            item["name"]=item["name"] if update_item.name is None else update_item.name
            item["email"]=item["email"] if update_item.email is None else update_item.email

            return item
        
@app.delete("/items/{id}",response_model=Optional[ItemResponse])
async def deleate(id :int):
    for i in range(len(items)):
        if items[i]["id"]==id:
            item=items.pop(i)
            return item
            