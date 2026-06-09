from redis_base.redis_client import create_redis_client
from redis_base.redis_config import RedisSettings


class RedisInitializer:
    def __init__(self):
        self.m_redis_client = None

    def init_redis(self, p_yml_cfg: dict):
        if "redis" not in p_yml_cfg:
            raise RuntimeError(f"Nacos 配置中缺少 redis 节点，当前配置：{p_yml_cfg}")

        print("Redis 配置已从 Nacos 加载：", p_yml_cfg["redis"])

        redis_config = RedisSettings(**p_yml_cfg["redis"])
        self.m_redis_client = create_redis_client(redis_config)

        self.m_redis_client.ping()

        return self.m_redis_client

    def close_redis(self):
        if self.m_redis_client is not None:
            self.m_redis_client.close()
            self.m_redis_client = None