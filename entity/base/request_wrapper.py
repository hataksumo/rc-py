from datetime import datetime
from typing import TypeVar, Generic
from uuid import uuid4

from pydantic import BaseModel, Field


T = TypeVar("T")


class CommonParams(BaseModel):
    interfaceCode: str = Field(default="7000", description="接口编码")
    timeStamp: str = Field(default="", description="请求时间")
    transNo: str = Field(default="", description="交易流水号")


class RequestWrapper(BaseModel, Generic[T]):
    commonParams: CommonParams
    reqParams: T

    @classmethod
    def of(cls, p_data: T) -> "RequestWrapper[T]":
        common_params = CommonParams(
            interfaceCode="0000",
            timeStamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            transNo=str(uuid4()),
        )

        return cls(
            commonParams=common_params,
            reqParams=p_data,
        )

    @classmethod
    def of(cls, p_interfaceCode:str ,p_transNo:str, p_data: T) -> "RequestWrapper[T]":
        common_params = CommonParams(
            interfaceCode=p_interfaceCode,
            timeStamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            transNo=str(p_transNo),
        )

        return cls(
            commonParams=common_params,
            reqParams=p_data,
        )