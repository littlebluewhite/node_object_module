from pydantic import BaseModel

import schemas.device_info


class NodeBaseBasic(BaseModel):
    name: str
    description: str | None = None
    value: str | None = None
    node_type: str | None = None


class NodeBase(NodeBaseBasic):
    id: int

    device_info: schemas.device_info.DeviceInfo | None = None

    class Config:
        orm_mode = True


class NodeBaseCreate(NodeBaseBasic):
    pass


class NodeBaseUpdate(NodeBaseBasic):
    # uid: str | None = None
    node_type: str | None = None
    name: str | None = None # Make it optional in APINodeUpdate


class NodeBaseMultipleUpdate(NodeBaseUpdate):
    id: int
