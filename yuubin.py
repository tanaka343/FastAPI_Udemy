from fastapi import FastAPI

app = FastAPI()

adress=[{
    "zipcode": "1000001",
    "prefcode": "13",
    "address1": "東京都",   
    "address2": "千代田区",   
    "address3": "千代田"      
  }]

@app.get("/")
async def find_adress(zipcode :str):
    for i in adress:
        if i["zipcode"]==zipcode:
            return i
