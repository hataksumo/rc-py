from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    rtnCode: str
    object: T
    rtnMsg: str

    @classmethod
    def ok(cls, p_data: T|None = None) -> "ResponseWrapper[T]":
        return cls(
            rtnCode="0",
            rtnMsg="success",
            object=p_data,
        )

    @classmethod
    def fail(
            cls,
            pRtnCode: str = "500",
            pRtnMsg: str = "系统异常",
    ) -> "ResponseWrapper[None]":
        return cls(
            rtnCode=pRtnCode,
            rtnMsg=pRtnMsg,
            object=None,
        )