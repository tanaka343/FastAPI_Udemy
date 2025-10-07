from fastapi import APIRouter,Body
from cruds import item as item_cruds
from schemas import ItemCreate

#prefix共通設定
router = APIRouter(prefix="/items",tags=["Items"])

@router.get("")
async def find_all():
    return item_cruds.find_all()

@router.get("/{id}")
async def find_by_id(id: int):
    return item_cruds.find_by_id(id)

@router.get("/")
async def find_by_name(name: str):
    return item_cruds.find_by_name(name)

@router.post("")
async def create(item_create: ItemCreate):
    return item_cruds.create(item_create)

@router.put("/{id}")
async def update(id :int,item_update = Body()):
    return item_cruds.updata(id,item_update)

@router.delete("/{id}")
async def delete(id :int):
    return item_cruds.delete(id)