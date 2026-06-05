from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List

import yaml

from config.redis_config import redis_config
from core import init_nacos_client, register_service, get_nacos_config, unregister_service, NACOS_DEFAULT_GROUP


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 【服务启动前执行】初始化Nacos + 注册服务 + 拉取Redis配置
    await init_nacos_client()
    await register_service()

    # 从Nacos拉取redis配置（示例data_id=fastapi-redis.yml）
    nacos_yaml = await get_nacos_config(data_id="python-serv-dev.yaml",group=NACOS_DEFAULT_GROUP)
    global redis_conf
    yml_cfg = yaml.safe_load(nacos_yaml)
    redis_config
    print("✅ Redis配置已从Nacos加载：", yml_cfg)

    yield # 应用运行中

    # 【服务关闭时执行】注销Nacos服务
    await unregister_service()

fengkong = FastAPI(lifespan=lifespan, title="工程化FastAPI-Nacos")




class AnalysisRequest(BaseModel):
    rule_id: int
    start_time: str
    end_time: str
    conditions: Dict[str, Any]


class AnalysisResponse(BaseModel):
    success: bool
    message: str
    metric_count: int


@fengkong.post("/analysis/run", response_model=AnalysisResponse)
async def run_analysis(req: AnalysisRequest):
    # 1. 根据 req 组装 SQL
    # 2. 查询数据库
    # 3. 计算指标
    # 4. 写入 Redis

    return AnalysisResponse(
        success=True,
        message="ok",
        metric_count=10
    )