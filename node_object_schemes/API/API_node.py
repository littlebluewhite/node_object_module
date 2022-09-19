import datetime

import node_object_schemes.node_base
import node_object_schemes.third_dimension_instance
import node_object_schemes.device_info
from node_object_schemes.node import NodeBasic


class APINodeBaseCreate(node_object_schemes.node_base.NodeBaseCreate):
    device_info: node_object_schemes.device_info.DeviceInfoBasic | None = None


class APINode(NodeBasic):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    child_nodes: list[int] = list()
    node_groups: list[int] = list()
    objects: list[int] = list()

    node_base: node_object_schemes.node_base.NodeBase | None = None
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstance | None = None


class APINodeCreate(NodeBasic):
    node_base: APINodeBaseCreate
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstanceBasic | None = None
