"""
Core package: Nacos integration & service management
Public API: init_nacos_client, register_service, unregister_service, get_nacos_config
"""


from .app_context import app_context

# 明确公开接口，隐藏内部实现
__all__ = [
    "app_context"
]

# 包级常量（可选）
NACOS_DEFAULT_GROUP = "DEV"