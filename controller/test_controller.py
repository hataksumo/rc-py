from fastapi import FastAPI, Query, Depends, APIRouter, Path
from redis import Redis, RedisCluster

from core.dependencies import get_redis

test_router = APIRouter(prefix="/test")

@test_router.get("/value/{pKey}")
def get_value(
    pKey: str = Path(..., description="Redis key"),
    redis_client: Redis | RedisCluster = Depends(get_redis)
):
    return redis_client.get(pKey)