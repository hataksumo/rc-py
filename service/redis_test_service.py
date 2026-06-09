from redis import Redis, RedisCluster

from entity.test import RedisQueryResponse, RedisQueryRequest


class RedisTestService:
    def __init__(self, p_redis_client: Redis | RedisCluster):
        self.m_redis_client = p_redis_client

    def get_value(self, p_redis_request: RedisQueryRequest) -> RedisQueryResponse:
        data = self.m_redis_client.get(p_redis_request.key)

        return RedisQueryResponse(data=data)