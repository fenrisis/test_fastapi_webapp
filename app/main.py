from fastapi import FastAPI, Depends
from app.routers import data_router
from app.dependencies import get_redis

app = FastAPI(dependencies=[Depends(get_redis)])

app.include_router(data_router.router)
