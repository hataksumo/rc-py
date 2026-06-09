from contextlib import asynccontextmanager

from fastapi import FastAPI


from core.app_context import app_context
from mysql_base.mysql_initializer import MysqlInitializer
from nacos_base import init_nacos_client, register_service, NacosConfigLoader
from redis_base.redis_initializer import RedisInitializer


redis_initializer = RedisInitializer()
mysql_initializer = MysqlInitializer()


@asynccontextmanager
async def lifespan(p_app: FastAPI):
    try:
        # 1. 初始化 Nacos 客户端
        await init_nacos_client()

        # 2. 注册服务
        await register_service()

        # 3. 拉取 Nacos 配置
        config_loader = NacosConfigLoader()
        yml_cfg = await config_loader.load_config(
            p_data_id="python-serv-dev.yaml"
        )

        app_context.m_yml_cfg = yml_cfg

        # 4. 初始化 Redis
        redis_client = redis_initializer.init_redis(yml_cfg)
        app_context.m_redis_client = redis_client
        p_app.state.redis = redis_client

        # 5. 初始化 MySQL
        mysql_client = await mysql_initializer.init_mysql(yml_cfg)
        app_context.m_mysql_client = mysql_client
        p_app.state.mysql = mysql_client

        print("应用启动初始化完成")

        yield

    finally:
        await mysql_initializer.close_mysql()
        redis_initializer.close_redis()

        print("应用资源已释放")