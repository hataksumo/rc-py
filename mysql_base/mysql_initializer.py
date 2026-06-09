from mysql_base.mysql_client import MysqlClient
from mysql_base.mysql_config import MysqlConfig


class MysqlInitializer:
    def __init__(self):
        self.m_mysql_client = None

    async def init_mysql(self, p_yml_cfg: dict):
        if "mysql" not in p_yml_cfg:
            raise RuntimeError(f"Nacos 配置中缺少 mysql 节点，当前配置：{p_yml_cfg}")

        print("mysql 配置已从 Nacos 加载：", p_yml_cfg["mysql"])

        mysql_setting = MysqlConfig(**p_yml_cfg["mysql"])

        self.m_mysql_client = MysqlClient(mysql_setting)
        await self.m_mysql_client.init_pool()

        return self.m_mysql_client

    async def close_mysql(self):
        if self.m_mysql_client is not None:
            await self.m_mysql_client.close_pool()
            self.m_mysql_client = None