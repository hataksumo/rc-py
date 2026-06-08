from fastapi import FastAPI, Query, Depends, APIRouter, Path
from redis import Redis, RedisCluster

from core.dependencies import get_redis
from entity import RequestWrapper, ResponseWrapper
from entity.test import RedisQueryRequest, RedisQueryResponse

test_router = APIRouter(prefix="/test")

@test_router.post("/redis/get_value")
def get_value(
    pRequest: RequestWrapper[RedisQueryRequest],
    redis_client: Redis | RedisCluster = Depends(get_redis)
)->ResponseWrapper[RedisQueryResponse]:
    data = redis_client.get(pRequest.reqParams.key)
    rsp : RedisQueryResponse  = RedisQueryResponse(data=data)
    return ResponseWrapper.ok(rsp)