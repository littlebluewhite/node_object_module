import datetime

from pydantic import BaseModel


class NodeNodeGroup(BaseModel):
    node_id: int

    class Config:
        orm_mode = True


class NodeGroupBasic(BaseModel):
    name: str
    is_topics: bool = True
    description: str | None = None


class NodeGroup(NodeGroupBasic):
    id: int
    update_at: datetime.datetime

    nodes: list[NodeNodeGroup] = list()

    class Config:
        orm_mode = True


class NodeGroupCreate(NodeGroupBasic):
    pass


class NodeGroupUpdate(NodeGroupBasic):
    name: str | None = None
    is_topics: bool | None = None
    description: str | None = None


class NodeGroupMultipleUpdate(NodeGroupBasic):
    id: int
