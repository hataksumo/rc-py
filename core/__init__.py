"""
Core package: Nacos integration & service management
Public API: init_nacos_client, register_service, unregister_service, get_nacos_config
"""
from typing import Optional
from .nacos_sdk import (
    init_nacos_client,
    register_service,
    unregister_service,
    get_nacos_config,
    nacos_config_client,
    nacos_naming_client
)

# 明确公开接口，隐藏内部实现
__all__ = [
    "init_nacos_client",
    "register_service",
    "unregister_service",
    "get_nacos_config",
    "nacos_config_client",
    "nacos_naming_client"
]

# 包级常量（可选）
NACOS_DEFAULT_GROUP = "DEV"