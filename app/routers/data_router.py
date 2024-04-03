from fastapi import APIRouter, HTTPException, Depends
from app.models import Item
from app.dependencies import get_redis

router = APIRouter()


@router.post("/write_data/")
async def write_data(item: Item, redis=Depends(get_redis)):
    redis.set(item.phone, item.address)
    return {"message": "Data saved successfully"}


@router.get("/check_data/")
async def check_data(phone: str, redis=Depends(get_redis)):
    address = redis.get(phone)
    if not address:
        raise HTTPException(status_code=404, detail="Phone not found")
    return {"phone": phone, "address": address}