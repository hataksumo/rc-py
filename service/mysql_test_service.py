from entity.test import MysqlTestQueryRequest
from mysql_base import MysqlClient


class MysqlDemoService:
    def __init__(self, p_mysql_client: MysqlClient):
        self.m_mysql_client = p_mysql_client

    async def query_by_time_range(self, p_request: MysqlTestQueryRequest) -> list[dict]:
        if p_request.start_time >= p_request.end_time:
            raise ValueError("开始时间必须小于结束时间")

        sql = """
            select
                id,
                code,
                name,
                str_1,
                str_2,
                int_1,
                int_2,
                time_field
            from py_test
            where time_field >= %s
              and time_field < %s
            order by time_field asc, id asc
        """

        return await self.m_mysql_client.query_list(
            sql,
            (
                p_request.start_time,
                p_request.end_time,
            )
        )