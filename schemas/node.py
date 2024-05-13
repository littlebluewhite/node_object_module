import datetime

from pydantic import BaseModel

import schemas.third_dimension_instance
import schemas.node_base


class Object(BaseModel):
    id: int

    class Config:
        orm_mode = True


class NodeNodeGroup(BaseModel):
    node_group_id: int

    class Config:
        orm_mode = True


class ChildNode(BaseModel):
    id: int

    class Config:
        orm_mode = True


class NodeBasic(BaseModel):
    uid: str | None = None
    principal_name: str | None = None
    tags: list[str] = list()
    parent_node_id: int | None = None


class Node(NodeBasic):
    id: int
    tags: list[str]

    created_at: datetime.datetime
    updated_at: datetime.datetime

    node_base_id: int | None = None

    node_base: schemas.node_base.NodeBase | None = None
    child_nodes: list[ChildNode] = list()
    third_dimension_instance: schemas.third_dimension_instance.ThirdDimensionInstance | None = None
    node_groups: list[NodeNodeGroup] = list()
    objects: list[Object] = list()

    class Config:
        orm_mode = True


class NodeCreate(NodeBasic):
    node_base_id: int | None = None


class NodeUpdate(NodeBasic):
    node_base_id: int | None = None
    tags: list[str] | None = None


class NodeMultipleUpdate(NodeUpdate):
    id: int
    # helloworld: str
