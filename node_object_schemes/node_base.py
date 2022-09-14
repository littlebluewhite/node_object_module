from pydantic import BaseModel

import node_object_schemes.device_info


class NodeBaseBasic(BaseModel):
    description: str
    value: str
    node_type: str


class NodeBase(NodeBaseBasic):
    id: int

    device_info: node_object_schemes.device_info.DeviceInfo

    class Config:
        orm_mode = True


class NodeBaseCreate(NodeBaseBasic):
    pass


class NodeBaseUpdate(NodeBaseBasic):
    description: str | None = None
    value: str | None = None
    node_type: str | None = None


class NodeBaseMultipleUpdate(NodeBaseUpdate):
    id: int
