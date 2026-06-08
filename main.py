from contextlib import asynccontextmanager

from exceptiongroup import catch
from fastapi import FastAPI

import yaml

from controller import test_router
from redis_base import create_redis_client,RedisSettings
from core import init_nacos_client, register_service, get_nacos_config, unregister_service, NACOS_DEFAULT_GROUP


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 【服务启动前执行】初始化Nacos + 注册服务 + 拉取Redis配置
    await init_nacos_client()
    await register_service()

    # 从Nacos拉取redis配置（示例data_id=fastapi-redis_base.yml）
    # 【从 Nacos 配置中心读取配置】
    nacos_yaml = await get_nacos_config(
        data_id="python-serv-dev.yaml",
        group=NACOS_DEFAULT_GROUP,
    )

    print("Nacos 原始配置：", nacos_yaml)

    # 【把 Nacos YAML 转成 dict】
    yml_cfg = yaml.safe_load(nacos_yaml)

    if not yml_cfg:
        raise RuntimeError("Nacos 配置为空")

    if "redis" not in yml_cfg:
        raise RuntimeError(f"Nacos 配置中缺少 redis 节点，当前配置：{yml_cfg}")

    print("Redis 配置已从 Nacos 加载：", yml_cfg["redis"])

    # 【把 dict 转成 RedisSettings 对象】
    redis_settings = RedisSettings(**yml_cfg["redis"])

    # 【根据 RedisSettings 创建 Redis 客户端】
    redis_client = create_redis_client(redis_settings)
    redis_client.ping()

    # 【放到 FastAPI 应用上下文中，controller 通过 Depends(get_redis) 使用】
    app.state.redis = redis_client

    # 程序运行
    try:
        yield
    finally:
        redis_client.close()
        await unregister_service()


fengkong = FastAPI(
    title="fengkong",
    lifespan=lifespan,
)

fengkong.include_router(test_router)