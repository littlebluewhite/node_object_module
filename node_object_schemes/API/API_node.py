import datetime

import node_object_schemes.node_base
import node_object_schemes.third_dimension_instance
import node_object_schemes.device_info
from node_object_schemes.node import NodeBasic


class APINodeBase(node_object_schemes.node_base.NodeBaseBasic):
    device_info: node_object_schemes.device_info.DeviceInfoBasic | None = None


class API3DI(node_object_schemes.third_dimension_instance.ThirdDimensionInstanceBasic):
    update_at: datetime.datetime


class APINode(NodeBasic):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    child_nodes: list[int] = list()
    node_groups: list[int] = list()
    objects: list[int] = list()

    node_base: APINodeBase | None = None
    third_dimension_instance: API3DI | None = None


class APINodeBaseCreate(node_object_schemes.node_base.NodeBaseCreate):
    device_info: node_object_schemes.device_info.DeviceInfoBasic | None = None


class APINodeCreate(NodeBasic):
    node_base: APINodeBaseCreate
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstanceBasic | None = None


class APIDeviceInfoUpdate(node_object_schemes.device_info.DeviceInfoBasic):
    name: str | None = None
    company: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None


class APINodeBaseUpdate(node_object_schemes.node_base.NodeBaseUpdate):
    device_info: APIDeviceInfoUpdate | None = None


class APINodeUpdate(NodeBasic):
    node_id: str | None = None
    name: str | None = None
    tags: list[str] | None = None
    node_base: APINodeBaseUpdate | None = None
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstanceUpdate | None = None

