# config/settings.py
from pydantic_settings import BaseSettings

class NacosSettings(BaseSettings):
    # Nacos连接地址
    nacos_server: str = "localhost:8848"
    namespace_id: str = "ai-risk-controll-risk-dev"
    nacos_group: str = "DEV"
    nacos_user: str = "nacos"
    nacos_pwd: str = "nacos"
    grpc_timeout: int = 5000

    # 当前服务注册信息
    service_name: str = "fastapi-demo"
    service_port: int = 8000

nacos_cfg = NacosSettings()