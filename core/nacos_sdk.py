# core/nacos_sdk.py
import socket
from typing import Optional
# 你的异步nacos依赖
from v2.nacos import NacosNamingService, ClientConfigBuilder, GRPCConfig, NacosConfigService, ConfigParam, \
    RegisterInstanceParam
from config.settings import nacos_cfg

# 全局单例，项目全局共用
nacos_config_client: Optional[NacosConfigService] = None
nacos_naming_client: Optional[NacosNamingService] = None
# 本机注册IP（自动获取局域网IP）
SERVER_IP = socket.gethostbyname(socket.gethostname())

async def init_nacos_client():
    """初始化Nacos【配置中心+注册中心】客户端（异步，在lifespan调用）"""
    global nacos_config_client, nacos_naming_client
    # 构造客户端配置
    client_config = (
        ClientConfigBuilder()
        .server_address(nacos_cfg.nacos_server)
        .namespace_id(nacos_cfg.namespace_id)
        .log_level("INFO")
        .grpc_config(GRPCConfig(grpc_timeout=nacos_cfg.grpc_timeout))
        .build()
    )
    # 初始化配置中心客户端
    nacos_config_client = await NacosConfigService.create_config_service(client_config)
    # 初始化注册中心（服务发现）客户端
    nacos_naming_client = await NacosNamingService.create_naming_service(client_config)
    print("✅ Nacos 配置&注册客户端初始化完成")

async def register_service():
    """服务注册到Nacos注册中心"""
    global nacos_naming_client

    register_request:RegisterInstanceParam = RegisterInstanceParam(
        service_name=nacos_cfg.service_name,
        ip=SERVER_IP,
        port=nacos_cfg.service_port,
        healthy=True,
        enable=True
    )

    await nacos_naming_client.register_instance(
        register_request
    )
    print(f"✅ 服务 {nacos_cfg.service_name} {SERVER_IP}:{nacos_cfg.service_port} 注册成功")

async def unregister_service():
    """服务下线注销"""
    global nacos_naming_client
    deregister_request = RegisterInstanceParam(
        service_name=nacos_cfg.service_name,
        ip=SERVER_IP,
        port=nacos_cfg.service_port
    )
    await nacos_naming_client.deregister_instance(deregister_request)
    print(f"✅ 服务 {nacos_cfg.service_name} 从Nacos注销完成")

async def get_nacos_config(data_id: str, group: str = "DEV") -> str:
    """从Nacos配置中心拉取配置内容"""
    global nacos_config_client
    get_config_request = ConfigParam(
        data_id=data_id, group=group, type="YAML"
    )
    content = await nacos_config_client.get_config(get_config_request)
    return content