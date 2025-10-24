from fastapi import FastAPI,Body

app = FastAPI()

items = [
  {"id":1,"name":"tanaka1"},
  {"id":2,"name":"tanaka2"},
  {"id":3,"name":"tanaka3"},
]

#READ処理

@app.get("/items")
async def find_all():
    return items


@app.get("/items/{id}")
async def find_by_id(id :int):
    for item in items:
        if item["id"]==id:
            return item
        

@app.get("/items/")
async def find_by_name(name :str):
    filtered_name=[]
    for item in items:
        if name in item["name"]:
            filtered_name.append(item)
    return filtered_name

@app.post("/items")
async def create(create_item=Body()):
    new_item={
        "id":len(items)+1,
        "name":create_item["name"],
    }
    items.append(new_item)
    return new_item

@app.put("/items/{id}")
async def update(id :int,update_item=Body()):
    for item in items:
        if item["id"]==id:
            item["name"]=update_item["name"]

            return item
        
@app.delete("/items/{id}")
async def deleate(id :int):
    for i in range(len(items)):
        if items[i]["id"]==id:
            item=items.pop(i)
            return item
            