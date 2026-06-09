from contextlib import asynccontextmanager

from fastapi import FastAPI

import yaml

from controller import test_router
from core.app_lifespan import lifespan



fengkong = FastAPI(
    title="fengkong",
    lifespan=lifespan,
)

fengkong.include_router(test_router)

@fengkong.get("/")
async def root():
    return {
        "success": True,
        "message": "fengkong service is running"
    }