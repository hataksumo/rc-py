from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class MysqlConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYSQL_",
        env_file=".env",
        extra="ignore"
    )

    host: str = "127.0.0.1"
    port: int = 3306
    username: str = "root"
    password: str = ""
    database: str = ""

    min_size: int = 2
    max_size: int = 10

    connect_timeout: int = 10


mysql_setting : Optional[MysqlConfig] = None