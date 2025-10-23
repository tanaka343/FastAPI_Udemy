from fastapi import FastAPI

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