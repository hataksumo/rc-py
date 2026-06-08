from pydantic import BaseModel


class RedisQueryRequest(BaseModel):
    key: str

class RedisQueryResponse(BaseModel):
    data: str|None