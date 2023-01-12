import datetime

from pydantic import BaseModel

import schemas.node_base
import schemas.third_dimension_instance
import schemas.device_info
from schemas.node import NodeBasic


class APINodeBase(schemas.node_base.NodeBaseBasic):
    device_info: schemas.device_info.DeviceInfoBasic | None = None


class API3DI(schemas.third_dimension_instance.ThirdDimensionInstanceBasic):
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


class APINodeSimple(BaseModel):
    id: int
    uid: str | None
    name: str | None


class APINodeBaseCreate(schemas.node_base.NodeBaseCreate):
    device_info: schemas.device_info.DeviceInfoBasic | None = None


class APINodeCreate(NodeBasic):
    node_base: APINodeBaseCreate
    third_dimension_instance: schemas.third_dimension_instance.ThirdDimensionInstanceBasic | None = None


class APIDeviceInfoUpdate(schemas.device_info.DeviceInfoBasic):
    company: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None


class APINodeBaseUpdate(schemas.node_base.NodeBaseUpdate):
    device_info: APIDeviceInfoUpdate | None = None


class APINodeUpdate(NodeBasic):
    node_id: str | None = None
    tags: list[str] | None = None
    node_base: APINodeBaseUpdate = APINodeBaseUpdate()
    third_dimension_instance: schemas.third_dimension_instance.ThirdDimensionInstanceBasic | None = None


class APINodeMultipleUpdate(APINodeUpdate):
    id: int
