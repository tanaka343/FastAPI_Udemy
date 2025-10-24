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

##nameすべて一致     
@app.get("/items/")
async def find_by_name(name :str):
   for item in items:
      if item["name"]==name:
         return item

##name一部一致
@app.get("/items//")
async def find_by_name2(name :str):
    filtered_name = []
    for item in items:
      if name in item["name"]:
         filtered_name.append(item)
    return filtered_name


@app.post("/items")
async def create(new_item=Body()):
   new_item={
      "id":len(items)+1,
      "name":new_item["name"]
   }
   items.append(new_item)
   return new_item

@app.put("/items/{id}")
async def update(id :int,update_item=Body()):
   for item in items:
      if item["id"]==id:
         item["name"]= update_item["name"]
         return item
      
@app.delete("/items/{id}")
async def delete(id :int):
   for i in range(len(items)):
      if items[i]["id"]==id:
         delete_item=items.pop(i)
         return delete_item