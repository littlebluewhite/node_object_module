import datetime

from pydantic import BaseModel

import node_object_schemes.third_dimension_instance
import node_object_schemes.node_base


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
    node_id: str
    principal_name: str | None = None
    tags: list[str] = list()
    parent_node_id: int | None = None


class Node(NodeBasic):
    id: int
    tags: list[str]

    create_at: datetime.datetime
    update_at: datetime.datetime

    node_base_id: int | None = None

    node_base: node_object_schemes.node_base.NodeBase | None = None
    child_nodes: list[ChildNode] = list()
    third_dimension_instance: node_object_schemes.third_dimension_instance.ThirdDimensionInstance | None = None
    node_groups: list[NodeNodeGroup] = list()
    objects: list[Object] = list()

    class Config:
        orm_mode = True


class NodeCreate(NodeBasic):
    node_base_id: int | None = None


class NodeUpdate(NodeBasic):
    node_id: str | None = None
    node_base_id: int | None = None
    tags: list[str] | None = None


class NodeMultipleUpdate(NodeUpdate):
    id: int
