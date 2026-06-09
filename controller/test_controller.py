from fastapi import FastAPI, Query, Depends, APIRouter, Path, HTTPException
from redis import Redis, RedisCluster

from core.dependencies import get_redis, get_redis_test_service, get_mysql_demo_service
from entity import RequestWrapper, ResponseWrapper
from entity.test import RedisQueryRequest, RedisQueryResponse, MysqlTestQueryRequest
from service.mysql_test_service import MysqlDemoService
from service.redis_test_service import RedisTestService

test_router = APIRouter(prefix="/test")

@test_router.post("/redis/get_value")
def get_value(
    pRequest: RequestWrapper[RedisQueryRequest],
    p_service: RedisTestService = Depends(get_redis_test_service)
)->ResponseWrapper[RedisQueryResponse]:
    data = p_service.get_value(pRequest.reqParams)
    rsp : RedisQueryResponse  = RedisQueryResponse(data=data)
    return ResponseWrapper.ok(rsp)

@test_router.post("/mysql/py_test/query-by-time")
async def query_by_time(
        p_request: RequestWrapper[MysqlTestQueryRequest],
        p_service: MysqlDemoService = Depends(get_mysql_demo_service)
) ->ResponseWrapper:
    try:
        data_list = await p_service.query_by_time_range(p_request.reqParams)
        return ResponseWrapper.ok(data_list)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )