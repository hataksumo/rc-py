from redis import Redis, ConnectionPool
from redis.cluster import RedisCluster, ClusterNode

from redis_base.redis_config import RedisSettings


def create_redis_client(pSettings: RedisSettings):
    if pSettings.mode == "single":
        pool = ConnectionPool(
            host=pSettings.host,
            port=pSettings.port,
            db=pSettings.db,
            password=pSettings.password or None,
            decode_responses=pSettings.decode_responses,
            socket_timeout=pSettings.socket_timeout,
            socket_connect_timeout=pSettings.socket_connect_timeout,
            max_connections=pSettings.max_connections,
        )
        return Redis(connection_pool=pool)

    if pSettings.mode == "cluster":
        startup_nodes = [
            ClusterNode(host=node.host, port=node.port)
            for node in pSettings.startup_nodes
        ]

        if not startup_nodes:
            raise RuntimeError("Redis cluster mode requires redis_base.startup_nodes")

        return RedisCluster(
            startup_nodes=startup_nodes,
            password=pSettings.password or None,
            decode_responses=pSettings.decode_responses,
            socket_timeout=pSettings.socket_timeout,
            socket_connect_timeout=pSettings.socket_connect_timeout,
            max_connections=pSettings.max_connections,
        )

    raise RuntimeError(f"Unsupported redis_base mode: {pSettings.mode}")