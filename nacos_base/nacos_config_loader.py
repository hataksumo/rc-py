import yaml

from core import NACOS_DEFAULT_GROUP
from nacos_base.nacos_sdk import get_nacos_config


class NacosConfigLoader:
    def __init__(self):
        pass

    async def load_config(self, p_data_id: str, p_group: str = NACOS_DEFAULT_GROUP) -> dict:
        nacos_yaml = await get_nacos_config(
            data_id=p_data_id,
            group=p_group,
        )

        print("Nacos 原始配置：", nacos_yaml)

        yml_cfg = yaml.safe_load(nacos_yaml)

        if not yml_cfg:
            raise RuntimeError("Nacos 配置为空")

        return yml_cfg