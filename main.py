from fastapi import FastAPI

app = FastAPI()

items =[
    {"id":1,"name":"tanaka"},
    {"id":2,"name":"satou"},
]


@app.get("/")
async def sanple(items):
    return items