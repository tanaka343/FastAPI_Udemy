from fastapi import FastAPI

app = FastAPI()

items = [
  {"id":1,"name":"tanaka1"},
  {"id":2,"name":"tanaka2"},
  {"id":3,"name":"tanaka3"},
]

@app.get("/{id}")
async def top(id: int):
  for item in items:
    if item["id"]==id:
        return item["name"]