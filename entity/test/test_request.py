from datetime import datetime

from pydantic import BaseModel, Field


class RedisQueryRequest(BaseModel):
    key: str

class RedisQueryResponse(BaseModel):
    data: str|None

class MysqlTestQueryRequest(BaseModel):
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")