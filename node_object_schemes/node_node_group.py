from pydantic import BaseModel


class NodeNodeGroupBasic(BaseModel):
    node_id: int
    node_group_id: int


class NodeNodeGroup(NodeNodeGroupBasic):
    id: int

    class Config:
        orm_mode = True


class NodeNodeGroupCreate(NodeNodeGroupBasic):
    pass


class NodeNodeGroupUpdate(NodeNodeGroupBasic):
    node_id: int | None = None
    node_group_id: int | None = None


class NodeNodeGroupMultipleUpdate(NodeNodeGroupUpdate):
    id: int
