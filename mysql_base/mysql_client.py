from datetime import datetime, date
from typing import Any, Optional

import asyncmy
from asyncmy.cursors import DictCursor

from mysql_base.mysql_config import MysqlConfig


class MysqlClient:
    def __init__(self, pConfig: MysqlConfig):
        self.m_config = pConfig
        self.m_pool: Optional[asyncmy.Pool] = None

    async def init_pool(self):
        if self.m_pool is not None:
            return

        self.m_pool = await asyncmy.create_pool(
            host=self.m_config.host,
            port=self.m_config.port,
            user=self.m_config.username,
            password=self.m_config.password,
            db=self.m_config.database,
            minsize=self.m_config.min_size,
            maxsize=self.m_config.max_size,
            connect_timeout=self.m_config.connect_timeout,
            autocommit=True,
            charset="utf8mb4"
        )

    async def close_pool(self):
        if self.m_pool is None:
            return

        self.m_pool.close()
        await self.m_pool.wait_closed()
        self.m_pool = None

    def _check_pool(self):
        if self.m_pool is None:
            raise RuntimeError("Mysql connection pool is not initialized")


    async def query_list(self, p_sql: str, p_params: tuple | list | None = None) -> list[dict]:
        self._check_pool()

        params = p_params

        async with self.m_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(p_sql, params)
                result = await cursor.fetchall()
                return list(result)

    async def query_one(self, pSql: str, pParams: Optional[tuple | list] = None) -> Optional[dict[str, Any]]:
        self._check_pool()

        async with self.m_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(pSql, pParams or ())
                return await cursor.fetchone()

    async def execute(self, pSql: str, pParams: Optional[tuple | list] = None) -> int:
        self._check_pool()

        async with self.m_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(pSql, pParams or ())
                return cursor.rowcount

    async def execute_many(self, pSql: str, pParamsList: list[tuple | list]) -> int:
        self._check_pool()

        async with self.m_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(pSql, pParamsList)
                return cursor.rowcount

    async def transaction_execute(self, pSqlList: list[tuple[str, tuple | list | None]]):
        self._check_pool()

        async with self.m_pool.acquire() as conn:
            try:
                await conn.begin()

                async with conn.cursor() as cursor:
                    for sql, params in pSqlList:
                        await cursor.execute(sql, params or ())

                await conn.commit()

            except Exception:
                await conn.rollback()
                raise