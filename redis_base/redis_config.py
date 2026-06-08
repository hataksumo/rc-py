from pydantic_settings import BaseSettings
from pydantic import Field, validator, BaseModel
from typing import Optional, Literal



class RedisNodeSettings(BaseModel):
    host: str
    port: int

class RedisSettings(BaseModel):
    mode: Literal["single", "cluster"] = "single"

    host: str = "127.0.0.1"
    port: int = 6379
    db: int = 0

    startup_nodes: list[RedisNodeSettings] = []

    password: str | None = None
    decode_responses: bool = True
    socket_timeout: int = 3
    socket_connect_timeout: int = 3
    max_connections: int = 50


redis_config: Optional[RedisSettings] = None