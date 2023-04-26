import datetime

from pydantic import BaseModel


class APINode(BaseModel):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    child_nodes: list[int] = list()
    objects: list[int] = list()


class APINodeNodeGroup(BaseModel):
    node_id: int

    class Config:
        orm_mode = True


class APINodeGroupBasic(BaseModel):
    name: str
    is_topics: bool = True
    description: str | None = None


class APINodeGroup(APINodeGroupBasic):
    id: int
    update_at: datetime.datetime

    nodes: list[APINodeNodeGroup] = list()

    class Config:
        orm_mode = True


class APINodeGroupCreate(APINodeGroupBasic):
    node_ids: list[int] = []

class APINodeGroupUpdate(APINodeGroupBasic):
    name: str | None = None
    is_topics: bool | None = None
    description: str | None = None
    node_ids: list[int] = [4, 8, -2]


class APINodeGroupMultipleUpdate(APINodeGroupBasic):
    id: int
