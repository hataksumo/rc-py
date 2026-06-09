from fastapi import Request

from mysql_base import MysqlClient
from service import RedisTestService
from service.mysql_test_service import MysqlDemoService


def get_redis(request: Request):
    return request.app.state.redis

def get_redis_test_service(p_request: Request) -> RedisTestService:
    redis_client = p_request.app.state.redis
    return RedisTestService(redis_client)

def get_mysql(p_request: Request) -> MysqlClient:
    return p_request.app.state.mysql


def get_mysql_demo_service(p_request: Request) -> MysqlDemoService:
    mysql_client = p_request.app.state.mysql
    return MysqlDemoService(mysql_client)