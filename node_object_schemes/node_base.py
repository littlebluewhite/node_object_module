from pydantic import BaseModel

import node_object_schemes.device_info


class NodeBaseBasic(BaseModel):
    name: str
    description: str
    value: str
    node_type: str


class NodeBase(NodeBaseBasic):
    id: int

    device_info: node_object_schemes.device_info.DeviceInfo | None = None

    class Config:
        orm_mode = True


class NodeBaseCreate(NodeBaseBasic):
    pass


class NodeBaseUpdate(NodeBaseBasic):
    name: str | None = None
    description: str | None = None
    value: str | None = None
    node_type: str | None = None


class NodeBaseMultipleUpdate(NodeBaseUpdate):
    id: int
