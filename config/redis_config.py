from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional


class RedisConfig(BaseSettings):
    """Redis配置"""
    host: str = Field(..., description="地址")
    port: int = Field(6379, description="端口")
    passwd: str = Field(..., description="密码")


    def init(self,yml_cfg):
        self.url = yml_cfg.url
        self.namespace_id = yml_cfg.namespace_id
        self.namespace_name = yml_cfg.namespace_name



redis_config: Optional[RedisConfig] = None